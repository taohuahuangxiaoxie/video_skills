"""Preprocess before real Video Depth Anything temporal inference."""
import argparse
from fractions import Fraction
import gc
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'video-reference-prep/scripts'))
from video_ops import binary, digest, fitted_size, prepare_reference, probe, stream, verify_decode


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--workspace',type=Path,default=Path(os.environ.get('COMFYUI_WORKSPACE', str(Path.cwd()))))
    p.add_argument('--model-root',type=Path);p.add_argument('--checkpoint',type=Path)
    p.add_argument('--ffmpeg');p.add_argument('--ffprobe')
    p.add_argument('--prepared',action='store_true');p.add_argument('--cuts',default='')
    p.add_argument('--input-size',type=int,default=392);p.add_argument('--threads',type=int,default=6)
    a=p.parse_args(); source=a.input.resolve(); output=a.output.resolve()
    if output.exists() or source==output: raise FileExistsError(output)
    work=output.parent/(output.stem+'_work')
    if work.exists(): raise FileExistsError(f'Choose a new output name; working directory already exists: {work}')
    work.mkdir(parents=True)
    suffix='.exe' if os.name=='nt' else ''
    ffmpeg=binary('ffmpeg',a.ffmpeg or str(a.workspace/f'tools/ffmpeg/bin/ffmpeg{suffix}'))
    ffprobe=binary('ffprobe',a.ffprobe or str(a.workspace/f'tools/ffmpeg/bin/ffprobe{suffix}'))
    # Preprocessing is deliberately BEFORE loading torch, checkpoint or model.
    if a.prepared:
        prepared=source; preparation=None
    else:
        preparation=prepare_reference(source,output_path_arg=work/'source_ref_24fps_silent.mp4',ffmpeg=ffmpeg,ffprobe=ffprobe)
        prepared=Path(preparation['output'])
    info=probe(prepared,ffprobe); v=stream(info); frames_info=probe(prepared,ffprobe,True)['frames']
    tb=Fraction(v['time_base']); count=len(frames_info)
    assert count>0 and Fraction(v['avg_frame_rate'])==24
    assert max(abs(int(f['best_effort_timestamp'])*tb-Fraction(i,24)) for i,f in enumerate(frames_info))<=tb
    assert not any(s['codec_type']=='audio' for s in info['streams'])
    assert fitted_size(v)==(v['width'],v['height']),'Prepared source exceeds low-resolution bounds or has non-square pixel/rotation metadata.'
    cuts=[0]+sorted(set(int(x) for x in a.cuts.split(',') if x.strip()))+[count]
    assert all(0<=x<=count for x in cuts) and all(b>a for a,b in zip(cuts,cuts[1:])),cuts
    print(json.dumps({'stage':'preprocessing_verified','source':str(source),'prepared':str(prepared),'size':[v['width'],v['height']],'fps':24,'frames':count}),flush=True)

    model_root=a.model_root or a.workspace/'tools/depth/source/Video-Depth-Anything-main'
    checkpoint=a.checkpoint or a.workspace/'tools/depth/checkpoints/video_depth_anything_vits.pth'
    if not model_root.is_dir() or not checkpoint.is_file(): raise FileNotFoundError('Local Video Depth Anything model/checkpoint unavailable.')
    sys.path.insert(0,str(model_root))
    import cv2
    import numpy as np
    import torch
    from video_depth_anything.video_depth import VideoDepthAnything
    torch.set_num_threads(a.threads);torch.set_num_interop_threads(1);cv2.setNumThreads(1)
    model=VideoDepthAnything(encoder='vits',features=64,out_channels=[48,96,192,384])
    model.load_state_dict(torch.load(checkpoint,map_location='cpu',weights_only=True),strict=True)
    model.eval()
    cap=cv2.VideoCapture(str(prepared))
    ew,eh=fitted_size(v,max_long=768,max_short=432)
    chunks=work/'depth_chunks';chunks.mkdir()
    previews=work/'previews';previews.mkdir()
    lower,upper=float('inf'),float('-inf');segments=[];started=time.perf_counter()
    for index,(start,end) in enumerate(zip(cuts,cuts[1:])):
        rgb=[]
        for frame_index in range(start,end):
            ok,frame=cap.read()
            if not ok: raise RuntimeError(f'Unexpected EOF at prepared frame {frame_index}')
            frame=cv2.resize(frame,(ew,eh),interpolation=cv2.INTER_AREA)
            rgb.append(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        print(json.dumps({'stage':'infer_shot','shot':index+1,'shots':len(cuts)-1,'start_frame':start,'end_frame_exclusive':end}),flush=True)
        depth,fps=model.infer_video_depth(np.stack(rgb),target_fps=24,input_size=a.input_size,device='cpu',fp32=True)
        assert fps==24 and depth.shape==(end-start,eh,ew) and np.isfinite(depth).all()
        path=chunks/f'shot_{index+1:03d}_{start}_{end}.npy'
        np.save(path,depth)
        lo,hi=float(depth.min()),float(depth.max());lower=min(lower,lo);upper=max(upper,hi)
        segments.append(dict(start_frame=start,end_frame_exclusive=end,path=str(path),min=lo,max=hi))
        (work/'progress.json').write_text(json.dumps(dict(completed_shots=index+1,total_shots=len(cuts)-1,elapsed_seconds=time.perf_counter()-started),indent=2),encoding='utf-8')
        del rgb,depth;gc.collect()
    assert not cap.read()[0],'Prepared frame count mismatch'
    cap.release();del model;gc.collect()
    assert upper>lower
    w,h=v['width'],v['height']
    cmd=[ffmpeg,'-hide_banner','-v','warning','-n','-f','rawvideo','-pixel_format','gray','-video_size',f'{w}x{h}',
         '-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    preview_indices={0,count//4,count//2,3*count//4,count-1,*cuts[1:-1]}
    try:
        for segment in segments:
            depths=np.load(segment['path'],mmap_mode='r')
            for j,depth in enumerate(depths):
                gray=np.rint(np.clip((depth-lower)/(upper-lower),0,1)*255).astype(np.uint8)
                gray=cv2.resize(gray,(w,h),interpolation=cv2.INTER_LINEAR)
                proc.stdin.write(gray.tobytes())
                index=segment['start_frame']+j
                if index in preview_indices: cv2.imwrite(str(previews/f'depth_{index:05d}.png'),gray)
            del depths
    finally:
        proc.stdin.close()
    if proc.wait()!=0: raise RuntimeError('Depth encode failed')
    result=probe(output,ffprobe); ov=stream(result); output_frames=probe(output,ffprobe,True)['frames']; otb=Fraction(ov['time_base'])
    assert len(output_frames)==count and (ov['width'],ov['height'])==(w,h) and Fraction(ov['avg_frame_rate'])==24
    assert not any(s['codec_type']=='audio' for s in result['streams'])
    assert max(abs(int(f['best_effort_timestamp'])*otb-Fraction(i,24)) for i,f in enumerate(output_frames))<=otb
    assert abs(float(ov['duration'])-count/24)<0.001
    report=dict(source=str(source),prepared_rgb=str(prepared),preparation=preparation,output=str(output),width=w,height=h,fps=24,
                frames=count,duration_seconds=count/24,audio_streams=0,model='Video Depth Anything Small/vits',
                checkpoint_sha256=digest(checkpoint),source_sha256=digest(source),output_sha256=digest(output),
                representation='estimated relative inverse depth; near bright, far dark',global_mapping=[lower,upper],per_frame_autocontrast=False,
                official_temporal_inference_unmodified=True,temporal_settings=dict(window=32,overlap=10,alignment_interpolation=8),
                source_cut_frames=cuts,segments=segments,estimation_size=[ew,eh],input_size=a.input_size,device='cpu',precision='float32',
                full_decode=verify_decode(output,ffmpeg),previews=str(previews),inference_seconds=time.perf_counter()-started)
    output.with_suffix('.depth.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'stage':'complete','output':str(output),'frames':count,'fps':24,'size':[w,h]},ensure_ascii=False),flush=True)


if __name__=='__main__': main()
