// All processing happens in the browser. Nothing is uploaded.
(function(){
  const $=id=>document.getElementById(id);
  const drop=$('drop'),file=$('file'),go=$('go'),kb=$('kb'),maxw=$('maxw'),fmt=$('fmt');
  let src=null,srcName='image';
  const fmtKB=b=>(b/1024).toFixed(1)+' KB';

  drop.addEventListener('click',()=>file.click());
  drop.addEventListener('dragover',e=>{e.preventDefault();drop.classList.add('over')});
  drop.addEventListener('dragleave',()=>drop.classList.remove('over'));
  drop.addEventListener('drop',e=>{e.preventDefault();drop.classList.remove('over');if(e.dataTransfer.files[0])load(e.dataTransfer.files[0])});
  file.addEventListener('change',()=>file.files[0]&&load(file.files[0]));

  function load(f){
    if(!/^image\//.test(f.type)){alert('Please choose an image file (JPG, PNG, WEBP).');return}
    srcName=f.name.replace(/\.[^.]+$/,'');
    const img=new Image();
    img.onload=()=>{src=img;go.disabled=false;$('picked').textContent=f.name+' · '+fmtKB(f.size)+' · '+img.naturalWidth+'×'+img.naturalHeight};
    img.src=URL.createObjectURL(f);
  }

  function encode(w,h,q,type){
    const c=document.createElement('canvas');c.width=w;c.height=h;
    const x=c.getContext('2d');
    if(type==='image/jpeg'){x.fillStyle='#fff';x.fillRect(0,0,w,h)}
    x.drawImage(src,0,0,w,h);
    return new Promise(r=>c.toBlob(r,type,q));
  }

  async function fit(target,type){
    let w=src.naturalWidth,h=src.naturalHeight;
    const mw=parseInt(maxw.value,10);
    if(mw>0&&w>mw){h=Math.round(h*mw/w);w=mw}
    for(let pass=0;pass<12;pass++){
      let lo=0.05,hi=0.95,best=null;
      for(let i=0;i<8;i++){
        const q=(lo+hi)/2,b=await encode(w,h,q,type);
        if(b.size<=target){best=b;lo=q}else hi=q;
      }
      if(best)return{blob:best,w,h};
      const s=await encode(w,h,0.05,type);
      const k=Math.max(0.5,Math.min(0.9,Math.sqrt(target/s.size)*0.95));
      w=Math.max(1,Math.round(w*k));h=Math.max(1,Math.round(h*k));
    }
    return null;
  }

  go.addEventListener('click',async()=>{
    if(!src)return;
    const target=parseFloat(kb.value)*1024;
    if(!(target>0)){alert('Enter a target size in KB.');return}
    go.disabled=true;go.textContent='Working…';
    const type=fmt.value;
    const r=await fit(target,type);
    go.disabled=false;go.textContent='Compress';
    if(!r){alert('Could not reach that size. Try a larger KB value.');return}
    const url=URL.createObjectURL(r.blob),ext=type==='image/webp'?'webp':'jpg';
    $('out').src=url;
    $('dl').href=url;$('dl').download=srcName+'-'+Math.round(target/1024)+'kb.'+ext;
    $('stats').innerHTML='<span class="ok">'+fmtKB(r.blob.size)+'</span><span>Target: '+fmtKB(target)+'</span><span>'+r.w+'×'+r.h+' px</span>';
    $('result').style.display='block';
    $('result').scrollIntoView({behavior:'smooth'});
  });
})();
