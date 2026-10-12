/* Small SVG chart kit for the TD SYNNEX briefing. Colors come from CSS tokens so both themes work. */
(function(){
  const NS='http://www.w3.org/2000/svg';
  const S=['var(--s1)','var(--s2)','var(--s3)','var(--s4)'];
  const el=(tag,attrs={},parent)=>{const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e;};
  const fmt=(v,u)=>{ if(v==null||isNaN(v))return '—';
    if(u==='$B') return '$'+(+v).toFixed(v>=100?0:1)+'B';
    if(u==='$M') return '$'+Math.round(v).toLocaleString()+'M';
    if(u==='%') return (+v).toFixed(v<10?2:1).replace(/\.?0+$/,m=>m.startsWith('.')?'':m)+'%';
    if(u==='x') return (+v).toFixed(1)+'×';
    return (+v).toLocaleString(); };
  const nice=(max)=>{const p=Math.pow(10,Math.floor(Math.log10(max)));const n=[1,2,2.5,5,10].map(m=>m*p).find(m=>m>=max/4);return n;};
  const ticks=(max)=>{const st=nice(max);const out=[];for(let v=0;v<=max+st*0.001;v+=st)out.push(+v.toFixed(6));if(out[out.length-1]<max)out.push(out[out.length-1]+st);return out;};

  const width=host=>Math.round(Math.max(320,Math.min(640,(host&&host.clientWidth)||640)));
  let tip;
  function tipShow(evt,html){ if(!tip){tip=document.createElement('div');tip.className='viz-tip';document.body.appendChild(tip);}
    tip.innerHTML=html;tip.hidden=false;const r=tip.getBoundingClientRect();
    let x=evt.clientX+14,y=evt.clientY+14; if(x+r.width>innerWidth-8)x=evt.clientX-r.width-14; if(y+r.height>innerHeight-8)y=evt.clientY-r.height-14;
    tip.style.left=x+'px';tip.style.top=y+'px'; }
  function tipHide(){ if(tip)tip.hidden=true; }
  function bindTip(node,html){ node.addEventListener('pointermove',e=>tipShow(e,html)); node.addEventListener('pointerleave',tipHide);
    node.setAttribute('tabindex','0'); node.addEventListener('focus',()=>{const b=node.getBoundingClientRect();tipShow({clientX:b.right,clientY:b.top},html)}); node.addEventListener('blur',tipHide); }

  function legend(host,names){ if(names.length<2)return; const lg=document.createElement('div');lg.className='viz-legend';
    names.forEach((n,i)=>{const s=document.createElement('span');s.innerHTML=`<i style="background:${S[i]}"></i>${n}`;lg.appendChild(s);}); host.appendChild(lg); }

  function table(host,cols,rows){ const d=document.createElement('details');d.className='viz-table';
    d.innerHTML='<summary>Show the numbers</summary>'; const w=document.createElement('div');w.className='tbl-wrap';
    let h='<table><thead><tr>'+cols.map(c=>`<th>${c}</th>`).join('')+'</tr></thead><tbody>';
    rows.forEach(r=>{h+='<tr>'+r.map((c,i)=>`<td${i?' class="num"':''}>${c}</td>`).join('')+'</tr>';}); h+='</tbody></table>';
    w.innerHTML=h; d.appendChild(w); host.appendChild(d); }

  /* Vertical grouped columns. spec: {categories, series:[{name,values}], unit, height, labelLast} */
  function columns(host,spec){
    const W=width(host),narrow=W<520,H=(spec.height||280)+(narrow?10:0),m={t:24,r:8,b:narrow?44:34,l:44};const iw=W-m.l-m.r,ih=H-m.t-m.b;
    const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':spec.aria||''},null);
    const max=Math.max(...spec.series.flatMap(s=>s.values.filter(v=>v!=null)));const tk=ticks(max);const top=tk[tk.length-1];
    const y=v=>m.t+ih-(v/top)*ih;
    tk.forEach(t=>{el('line',{x1:m.l,x2:W-m.r,y1:y(t),y2:y(t),class:t?'grid':'base'},svg);const tx=el('text',{x:m.l-8,y:y(t)+4,'text-anchor':'end',class:'tick'},svg);tx.textContent=fmt(t,spec.unit);});
    const n=spec.categories.length,band=iw/n,k=spec.series.length;const bw=Math.min(24,(band*0.7-(k-1)*2)/k);const gw=k*bw+(k-1)*2;
    spec.categories.forEach((c,i)=>{const cx=m.l+band*i+band/2;
      const lab=el('text',{x:cx,y:H-m.b+18,'text-anchor':'middle',class:'tick'+(spec.highlight===i?' strong':'')},svg);if(band<60&&c.includes(' ')){const ps=c.split(' ');ps.forEach((pt,pi)=>{const ts=el('tspan',{x:cx,dy:pi?14:0},lab);ts.textContent=pt;});}else lab.textContent=c;
      spec.series.forEach((s,j)=>{const v=s.values[i];if(v==null)return;const x=cx-gw/2+j*(bw+2);const h=ih*(v/top);
        const r=Math.min(4,bw/2,h);const p=`M${x},${y(0)}V${y(v)+r}Q${x},${y(v)} ${x+r},${y(v)}H${x+bw-r}Q${x+bw},${y(v)} ${x+bw},${y(v)+r}V${y(0)}Z`;
        const path=el('path',{d:p,style:`fill:${S[j]}`,class:'mark'+(s.est&&s.est[i]?' est':'')},svg);
        const hit=el('rect',{x:x-2,y:m.t,width:bw+4,height:ih,class:'hit'},svg);
        bindTip(hit,`<b>${c}</b><br>${s.name}: ${fmt(v,spec.unit)}${s.note&&s.note[i]?'<br><small>'+s.note[i]+'</small>':''}`);
        const lblOn=spec.series.some(q=>q.label)?s.label:true; if(lblOn&&((spec.labelLast&&i===n-1)||(spec.labelAll))){const t=el('text',{x:x+bw/2,y:y(v)-6,'text-anchor':'middle',class:'vlabel'},svg);t.textContent=fmt(v,spec.unit);}
      });});
    host.appendChild(svg); legend(host,spec.series.map(s=>s.name));
    table(host,['',...spec.series.map(s=>s.name)],spec.categories.map((c,i)=>[c,...spec.series.map(s=>fmt(s.values[i],spec.unit))]));
  }

  /* Line chart (single axis). spec: {categories, series:[{name,values}], unit, min, max} */
  function line(host,spec){
    const W=width(host),H=(spec.height||240)+(W<520?10:0),m={t:20,r:52,b:W<520?44:34,l:44};const iw=W-m.l-m.r,ih=H-m.t-m.b;
    const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':spec.aria||''});
    const lo=spec.min,hi=spec.max;const y=v=>m.t+ih-((v-lo)/(hi-lo))*ih;const n=spec.categories.length;const x=i=>m.l+(n===1?iw/2:i*iw/(n-1));
    (spec.ticks||[lo,hi]).forEach(t=>{el('line',{x1:m.l,x2:W-m.r,y1:y(t),y2:y(t),class:t===lo?'base':'grid'},svg);const tx=el('text',{x:m.l-8,y:y(t)+4,'text-anchor':'end',class:'tick'},svg);tx.textContent=spec.unit==='%'?(+t).toFixed(1)+'%':fmt(t,spec.unit);});
    spec.categories.forEach((c,i)=>{const t=el('text',{x:x(i),y:H-m.b+18,'text-anchor':'middle',class:'tick'},svg);if(W<520&&c.includes(' ')){c.split(' ').forEach((pt,pi)=>{const ts=el('tspan',{x:x(i),dy:pi?14:0},t);ts.textContent=pt;});}else t.textContent=c;});
    spec.series.forEach((s,j)=>{const pts=s.values.map((v,i)=>v==null?null:[x(i),y(v)]);
      let d='';pts.forEach((p,i)=>{if(!p)return;d+=(d&&pts[i-1]?'L':'M')+p[0]+','+p[1];});
      el('path',{d,class:'ln',style:`stroke:${S[j]}`},svg);
      pts.forEach((p,i)=>{if(!p)return;const last=i===pts.length-1;el('circle',{cx:p[0],cy:p[1],r:last?5:3.5,class:'dot',style:`fill:${S[j]}`},svg);
        const hit=el('circle',{cx:p[0],cy:p[1],r:14,class:'hit'},svg);bindTip(hit,`<b>${spec.categories[i]}</b><br>${s.name}: ${fmt(s.values[i],spec.unit)}`);
        if(last||(spec.labelIdx||[]).includes(i)){const t=el('text',{x:last?p[0]+10:p[0],y:last?p[1]+4:p[1]-10,'text-anchor':last?'start':'middle',class:'vlabel'},svg);t.textContent=fmt(s.values[i],spec.unit);}});
    });
    host.appendChild(svg); legend(host,spec.series.map(s=>s.name));
    table(host,['',...spec.series.map(s=>s.name)],spec.categories.map((c,i)=>[c,...spec.series.map(s=>fmt(s.values[i],spec.unit))]));
  }

  /* Horizontal stacked bars (absolute). spec: {rows:[{label, parts:[values]}], names, unit} */
  function stack(host,spec){
    const W=width(host),cmp=W<520,rowH=30,lh=cmp?20:0,gap=cmp?18:26,m={t:8,r:spec.pct?8:64,b:8,l:cmp?0:(spec.labelW||92)};const H=m.t+m.b+spec.rows.length*(rowH+gap+lh)-gap+10;const iw=W-m.l-m.r;
    const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':spec.aria||''});
    const max=spec.max||Math.max(...spec.rows.map(r=>r.parts.reduce((a,b)=>a+(b||0),0)));
    spec.rows.forEach((r,ri)=>{const yy=m.t+ri*(rowH+gap+lh)+lh;const tl=el('text',cmp?{x:0,y:yy-7,class:'tick strong'}:{x:m.l-10,y:yy+rowH/2+4,'text-anchor':'end',class:'tick strong'},svg);tl.textContent=r.label;
      let x0=m.l;const tot=r.parts.reduce((a,b)=>a+(b||0),0);
      r.parts.forEach((v,j)=>{if(!v)return;const w=(v/max)*iw;const wd=Math.max(0,w-2);
        const rect=el('rect',{x:x0,y:yy,width:wd,height:rowH,rx:j===r.parts.length-1?4:0,style:`fill:${S[j]}`,class:'mark'},svg);
        bindTip(rect,`<b>${r.label}</b><br>${spec.names[j]}: ${fmt(v,spec.unit)} (${Math.round(v/tot*100)}%)`);
        if(wd>(spec.pct?34:64)){const t=el('text',{x:x0+8,y:yy+rowH/2+4,class:'inlabel'+(j===2||j===3?' dark':'')},svg);t.textContent=spec.pct?Math.round(v/tot*100)+'%':fmt(v,spec.unit);}
        x0+=w;});
      if(!spec.pct){const tt=el('text',{x:x0+6,y:yy+rowH/2+4,class:'vlabel'},svg);tt.textContent=fmt(tot,spec.unit);}
    });
    host.appendChild(svg); legend(host,spec.names);
    table(host,['',...spec.names,'Total'],spec.rows.map(r=>[r.label,...r.parts.map(v=>fmt(v,spec.unit)),fmt(r.parts.reduce((a,b)=>a+(b||0),0),spec.unit)]));
  }

  /* Horizontal bars, optional ranges [lo,hi] and highlight. spec: {rows:[{label,value,lo,hi,hl,note}], unit, max} */
  function bars(host,spec){
    const W=width(host),cmp=W<520,rowH=spec.rowH||22,lh=cmp?18:0,gap=spec.gap||12,m={t:6+lh,r:cmp?100:96,b:6,l:cmp?0:(spec.labelW||150)};const H=m.t+m.b+spec.rows.length*(rowH+gap+lh)-gap-lh;const iw=W-m.l-m.r;
    const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':spec.aria||''});
    const max=spec.max||Math.max(...spec.rows.map(r=>r.hi!=null?r.hi:r.value));const x=v=>m.l+(v/max)*iw;
    if(!cmp)el('line',{x1:m.l,x2:m.l,y1:0,y2:H,class:'base'},svg);
    spec.rows.forEach((r,i)=>{const yy=m.t+i*(rowH+gap+lh);const lab=el('text',cmp?{x:0,y:yy-6,class:'tick'+(r.hl?' strong':'')}:{x:m.l-10,y:yy+rowH/2+4,'text-anchor':'end',class:'tick'+(r.hl?' strong':'')},svg);lab.textContent=r.label;
      const col=r.hl?S[0]:'var(--muted-mark)';
      if(r.lo!=null){ el('rect',{x:x(r.lo),y:yy+rowH*0.2,width:Math.max(2,x(r.hi)-x(r.lo)),height:rowH*0.6,rx:3,style:`fill:${col};opacity:.35`},svg);
        el('rect',{x:x(r.value)-1.5,y:yy,width:3,height:rowH,rx:1,style:`fill:${col}`},svg);}
      else { const w=Math.max(2,x(r.value)-m.l);const rr=Math.min(4,w);el('path',{d:`M${m.l},${yy}H${m.l+w-rr}Q${m.l+w},${yy} ${m.l+w},${yy+rr}V${yy+rowH-rr}Q${m.l+w},${yy+rowH} ${m.l+w-rr},${yy+rowH}H${m.l}Z`,style:`fill:${col}`,class:'mark'},svg);}
      const vt=el('text',{x:x(r.hi!=null?r.hi:r.value)+8,y:yy+rowH/2+4,class:'vlabel'},svg);vt.textContent=r.text?r.text:r.lo!=null?`${fmt(r.lo,spec.unit)}–${fmt(r.hi,spec.unit)}`:fmt(r.value,spec.unit);
      const hit=el('rect',{x:0,y:yy-gap/2-lh,width:W,height:rowH+gap+lh,class:'hit'},svg);
      bindTip(hit,`<b>${r.label}</b><br>${r.text?r.text:r.lo!=null?'Range '+fmt(r.lo,spec.unit)+'–'+fmt(r.hi,spec.unit)+', midpoint '+fmt(r.value,spec.unit):fmt(r.value,spec.unit)}${r.note?'<br><small>'+r.note+'</small>':''}`);
    });
    host.appendChild(svg);
    table(host,['',spec.valueName||'Value',...(spec.rows.some(r=>r.note)?['Note']:[])],spec.rows.map(r=>[r.label,r.text?r.text:r.lo!=null?`${fmt(r.lo,spec.unit)}–${fmt(r.hi,spec.unit)}`:fmt(r.value,spec.unit),...(spec.rows.some(q=>q.note)?[r.note||'']:[])]));
  }

  window.Viz={columns,line,stack,bars};
  document.addEventListener('DOMContentLoaded',()=>{ (window.CHARTS||[]).forEach(c=>{const host=document.getElementById(c.id);if(host)Viz[c.type](host.querySelector('.viz-body'),c.spec);}); });
})();
