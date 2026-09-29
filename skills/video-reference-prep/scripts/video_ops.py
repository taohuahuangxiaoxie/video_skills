"""Reference preparation and frame-exact generated-video finishing; stdlib + FFmpeg."""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess


def binary(name, explicit=None):
    workspace = Path(os.environ.get('COMFYUI_WORKSPACE', str(Path.cwd())))
    exe = name + ('.exe' if os.name == 'nt' else '')
    for p in [explicit, os.environ.get(name.upper()), shutil.which(name), workspace/'tools/ffmpeg/bin'/exe]:
        if p and Path(p).is_file():
            return str(Path(p).resolve())
    raise FileNotFoundError(f'{name} not found; specify --{name}.')


def run(args):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-8000:])
    return result.stdout


def probe(path, ffprobe, frames=False):
    args = [ffprobe, '-v', 'error']
    if frames:
        args += ['-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp,duration_time']
    else:
        args += ['-show_format','-show_streams','-count_frames']
    return json.loads(run(args+['-of','json',path]))


def stream(info):
    return next(s for s in info['streams'] if s['codec_type']=='video')


def display_size(v):
    sar = v.get('sample_aspect_ratio','1:1')
    ratio = Fraction(sar.replace(':','/')) if sar not in ('N/A','0:1') else Fraction(1)
    w,h = float(v['width']*ratio),float(v['height'])
    rotation = next((float(s['rotation']) for s in v.get('side_data_list',[]) if 'rotation' in s),float(v.get('tags',{}).get('rotate',0)))
    return (h,w) if abs(rotation % 180-90)<1 else (w,h)


def fitted_size(v, max_long=1024, max_short=576):
    w,h=display_size(v)
    if abs(w/h-1)<0.001:
        bw=bh=min(max_long,768)
    else:
        bw,bh=(max_short,max_long) if h>w else (max_long,max_short)
    scale=min(1,bw/w,bh/h)
    return max(2,int(w*scale)//2*2),max(2,int(h*scale)//2*2)


def unique_output(path):
    path=Path(path)
    if not path.exists(): return path
    for n in range(2,10000):
        candidate=path.with_name(f'{path.stem}_v{n}{path.suffix}')
        if not candidate.exists(): return candidate
    raise FileExistsError(path)


def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()


def metadata_hits(path):
    # Scan MP4 container boxes, not compressed mdat bytes which can coincidentally
    # contain short strings such as "aigc". Codec SEI is removed by the encoder path.
    terms=[b'aigc',b'lvmetainfo',b'usercomment',b'dreamina',b'produceid',b'propagateid',b'contentproducer',b'contentpropagator']
    found=set(); total=Path(path).stat().st_size
    with open(path,'rb') as f:
        while f.tell()<total:
            begin=f.tell();header=f.read(8)
            if len(header)!=8: raise ValueError('Truncated MP4 box header')
            size,kind=struct.unpack('>I4s',header);header_size=8
            if size==1:
                size=struct.unpack('>Q',f.read(8))[0];header_size=16
            elif size==0:
                size=total-begin
            if size<header_size or begin+size>total: raise ValueError('Invalid MP4 box size')
            if kind==b'mdat':
                f.seek(begin+size);continue
            remaining=size-header_size;tail=b''
            while remaining:
                block=f.read(min(1048576,remaining));remaining-=len(block)
                data=tail+block.lower()
                found.update(t.decode() for t in terms if t in data)
                tail=data[-64:]
    return sorted(found)


def video_duration(path, v, ffprobe):
    if v.get('duration') not in (None,'N/A'):
        return float(v['duration'])
    frames=probe(path,ffprobe,True)['frames'];tb=Fraction(v['time_base'])
    if not frames: raise ValueError('Source has no video frames')
    stamps=[int(f['best_effort_timestamp'])*tb for f in frames]
    last_duration=Fraction(frames[-1]['duration_time']) if frames[-1].get('duration_time') else (
        stamps[-1]-stamps[-2] if len(stamps)>1 else 1/Fraction(v['avg_frame_rate']))
    return float(stamps[-1]-stamps[0]+last_duration)


def verify_decode(path, ffmpeg):
    run([ffmpeg,'-hide_banner','-v','error','-xerror','-i',path,'-f','null','-'])
    return 'passed'


def output_path(source, requested, suffix):
    target=Path(requested).resolve() if requested else unique_output(source.with_name(source.stem+suffix))
    if target==source or target.exists(): raise FileExistsError(f'Refusing to overwrite {target}')
    return target


def save_report(target, report):
    target.with_suffix('.processing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def prepare_reference(input_path, output_path_arg=None, fps=24, max_long=1024, max_short=576,
                      ffmpeg=None, ffprobe=None, plan_only=False):
    ffmpeg=binary('ffmpeg',ffmpeg); ffprobe=binary('ffprobe',ffprobe)
    source=Path(input_path).resolve(); info=probe(source,ffprobe); v=stream(info)
    if v.get('color_transfer') in ('smpte2084','arib-std-b67'):
        raise ValueError('HDR source requires an explicit HDR-preserving or tone-mapping path before SDR conversion.')
    rate=Fraction(str(fps))
    if rate<=0 or min(max_long,max_short)<2: raise ValueError('Invalid rate/size limits.')
    w,h=fitted_size(v,max_long,max_short)
    target=output_path(source,output_path_arg,f'_ref_{w}x{h}_{float(rate):g}fps_silent.mp4')
    cmd=[ffmpeg,'-hide_banner','-v','warning','-nostdin','-n','-i',source,'-map','0:v:0',
         '-vf',f'setpts=PTS-STARTPTS,fps={rate}:round=near,scale={w}:{h}:flags=lanczos,setsar=1',
         '-an','-sn','-dn','-map_metadata','-1','-map_chapters','-1','-c:v','libx264','-preset','medium',
         '-crf','18','-pix_fmt','yuv420p','-fps_mode','cfr','-movflags','+faststart',target]
    report=dict(mode='reference',source=str(source),output=str(target),target_fps=str(rate),target_size=[w,h],command=list(map(str,cmd)))
    if plan_only: return report
    target.parent.mkdir(parents=True,exist_ok=True); run(cmd)
    result=probe(target,ffprobe); rv=stream(result); frames=probe(target,ffprobe,True)['frames']; tb=Fraction(rv['time_base'])
    if not frames: raise ValueError('No output frames.')
    error=max(abs(int(f['best_effort_timestamp'])*tb-Fraction(i,1)/rate) for i,f in enumerate(frames))
    assert (rv['width'],rv['height'])==(w,h)
    assert not any(s['codec_type']=='audio' for s in result['streams'])
    assert Fraction(rv['avg_frame_rate'])==rate and error<=tb
    source_duration=video_duration(source,v,ffprobe); duration=float(rv['duration'])
    if abs(duration-source_duration)>1/float(rate)+0.001: raise ValueError(f'Duration drift: {source_duration} -> {duration}')
    report.update(frames=len(frames),duration_seconds=duration,source_video_duration_seconds=source_duration,audio_streams=0,
                  max_frame_grid_error_seconds=float(error),full_decode=verify_decode(target,ffmpeg),source_sha256=digest(source),output_sha256=digest(target))
    return save_report(target,report)


def finish_generated(input_path, output_path_arg=None, head=1, tail=3, mute=False, ffmpeg=None, ffprobe=None, plan_only=False):
    ffmpeg=binary('ffmpeg',ffmpeg); ffprobe=binary('ffprobe',ffprobe)
    source=Path(input_path).resolve(); info=probe(source,ffprobe); v=stream(info)
    if v.get('color_transfer') in ('smpte2084','arib-std-b67') or int(v.get('bits_per_raw_sample','8') or 8)>8:
        raise ValueError('HDR/10-bit source needs a color-preserving path; do not blindly remove all SEI.')
    if v.get('pix_fmt') not in ('yuv420p','yuvj420p','yuv422p','yuv444p'):
        raise ValueError('Review color/alpha format before SDR H.264 conversion.')
    frames=probe(source,ffprobe,True)['frames']; n=len(frames)
    if min(head,tail)<0 or n<=head+tail: raise ValueError(f'{n} frames cannot retain content with head={head}, tail={tail}.')
    tb=Fraction(v['time_base']); stamps=[int(f['best_effort_timestamp'])*tb for f in frames]
    if any(b<=a for a,b in zip(stamps,stamps[1:])): raise ValueError('Invalid presentation timestamps.')
    stop=n-tail; start=stamps[head]
    end=stamps[stop] if tail else stamps[-1]+Fraction(frames[-1].get('duration_time') or str(stamps[-1]-stamps[-2] if n>1 else Fraction(1,24)))
    target=output_path(source,output_path_arg,'_trimmed_clean.mp4')
    filters=[f'[0:v:0]trim=start_frame={head}:end_frame={stop},setpts=PTS-STARTPTS[v]']; maps=['-map','[v]']
    audios=[] if mute else [s for s in info['streams'] if s['codec_type']=='audio']
    for i in range(len(audios)):
        filters.append(f'[0:a:{i}]atrim=start={float(start):.12f}:end={float(end):.12f},asetpts=PTS-{float(start):.12f}/TB[a{i}]')
        maps+=['-map',f'[a{i}]']
    cmd=[ffmpeg,'-hide_banner','-v','warning','-nostdin','-n','-copyts','-i',source,'-filter_complex',';'.join(filters),*maps,
         '-map_metadata','-1','-map_metadata:s:v','-1','-map_chapters','-1','-c:v','libx264','-preset','slow','-crf','16',
         '-pix_fmt','yuv420p','-fps_mode:v','passthrough','-enc_time_base:v',str(tb),'-video_track_timescale',str(tb.denominator),
         '-bsf:v','filter_units=remove_types=6','-fflags','+bitexact','-flags:v','+bitexact','-metadata','encoder=','-metadata:s:v','encoder=']
    cmd+=['-map_metadata:s:a','-1','-c:a','aac','-b:a','192k','-flags:a','+bitexact','-metadata:s:a','encoder='] if audios else ['-an']
    cmd+=['-movflags','+faststart',target]
    report=dict(mode='generated',source=str(source),output=str(target),source_frames=n,head_removed=head,tail_removed=tail,
                retained_source_frame_indexes_zero_based=[head,stop-1],source_start_seconds=float(start),source_end_seconds=float(end),command=list(map(str,cmd)))
    if plan_only: return report
    target.parent.mkdir(parents=True,exist_ok=True); run(cmd)
    result=probe(target,ffprobe); rv=stream(result); rf=probe(target,ffprobe,True)['frames']; rtb=Fraction(rv['time_base'])
    assert len(rf)==stop-head,(len(rf),stop-head)
    error=max(abs(int(f['best_effort_timestamp'])*rtb-(expected-start)) for f,expected in zip(rf,stamps[head:stop]))
    assert error<=max(tb,rtb),error
    dw,dh=display_size(v); assert (rv['width'],rv['height'])==(round(dw),round(dh))
    new_audio=[s for s in result['streams'] if s['codec_type']=='audio']; assert len(new_audio)==len(audios)
    for track in new_audio: assert float(track.get('duration',0))<=float(end-start)+0.05
    tags=[result['format'].get('tags',{})]+[s.get('tags',{}) for s in result['streams']]
    hits=metadata_hits(target); assert not hits,hits
    assert not any(k.lower() in ('comment','aigc','lvmetainfo','usercomment') for t in tags for k in t)
    report.update(output_frames=len(rf),width=rv['width'],height=rv['height'],duration_seconds=float(result['format']['duration']),
                  max_retained_pts_error_seconds=float(error),audio_streams=len(new_audio),output_tags=tags,remaining_generation_metadata=hits,
                  full_decode=verify_decode(target,ffmpeg),source_sha256=digest(source),output_sha256=digest(target),
                  cleanup_scope='Container metadata and H.264 SEI; not visual/pixel watermark removal')
    return save_report(target,report)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['reference','finish']);p.add_argument('input',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--ffmpeg');p.add_argument('--ffprobe')
    p.add_argument('--fps',default='24');p.add_argument('--max-long',type=int,default=1024);p.add_argument('--max-short',type=int,default=576)
    p.add_argument('--head',type=int,default=1);p.add_argument('--tail',type=int,default=3);p.add_argument('--mute',action='store_true')
    p.add_argument('--plan-only',action='store_true');a=p.parse_args()
    common=dict(output_path_arg=a.output,ffmpeg=a.ffmpeg,ffprobe=a.ffprobe,plan_only=a.plan_only)
    report=prepare_reference(a.input,fps=a.fps,max_long=a.max_long,max_short=a.max_short,**common) if a.mode=='reference' else finish_generated(a.input,head=a.head,tail=a.tail,mute=a.mute,**common)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
