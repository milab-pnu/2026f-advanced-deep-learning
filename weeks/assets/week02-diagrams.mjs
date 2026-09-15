// 2주차 본문의 교육용 수치·배치를 독립적으로 시각화한다.
// 원논문 그림의 표현을 복제하지 않는다. 개념 출처는 각 Figure와 본문에 기재한다.
// 재생성: node weeks/assets/week02-diagrams.mjs
import { writeFileSync } from 'node:fs';
const out = new URL('./', import.meta.url);
const ink = '#0f172a', mid = '#64748b', line = '#94a3b8', pale = '#f8fafc';
const esc = s => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
let p;
function start(h, title) {
  p = [`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 ${h}" role="img" aria-label="${esc(title)}" font-family="system-ui, sans-serif">`, `<title>${esc(title)}</title>`, `<rect width="800" height="${h}" fill="white"/>`];
}
function rect(x,y,w,h,fill=pale,stroke=line,rx=4) { p.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}"/>`); }
function text(x,y,t,size=18,anchor='start',fill=ink,bold=false) { p.push(`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${fill}"${bold?' font-weight="600"':''}>${esc(t)}</text>`); }
function arrow(x1,y1,x2,y2,dashed=false) {
  const a=Math.atan2(y2-y1,x2-x1), l=7;
  p.push(`<path d="M${x1} ${y1} L${x2} ${y2}" fill="none" stroke="${ink}" stroke-width="1.5"${dashed?' stroke-dasharray="5 4"':''}/>`);
  p.push(`<polygon points="${x2},${y2} ${x2-l*Math.cos(a-.45)},${y2-l*Math.sin(a-.45)} ${x2-l*Math.cos(a+.45)},${y2-l*Math.sin(a+.45)}" fill="${ink}"/>`);
  if(dashed) p.push(`<polygon points="${x1},${y1} ${x1+l*Math.cos(a-.45)},${y1+l*Math.sin(a-.45)} ${x1+l*Math.cos(a+.45)},${y1+l*Math.sin(a+.45)}" fill="${ink}"/>`);
}
function save(name) { writeFileSync(new URL(name,out),p.join('\n')+'\n</svg>\n'); }

// 같은 노드를 같은 위치에 놓고, 통신 역할만 바꿔 비교한다.
start(560,'64 GPU의 두 배치: TP 8 DP 8과 TP 8 PP 4 DP 2');
function node(x,y,n,label) {
  rect(x,y,150,64);
  text(x+75,y+23,`N${n} · ${label}`,16,'middle',ink,true);
  for(let g=0;g<8;g++) { rect(x+8+g*17,y+34,15,21,'#e2e8f0',line,2); text(x+15.5+g*17,y+49,g,13,'middle'); }
}
for(const [off,kind] of [[0,'A'],[400,'B']]) {
  text(off+200,27,`구성 ${kind}`,22,'middle',ink,true);
  text(off+200,55,kind==='A'?'TP=8 · PP=1 · DP=8':'TP=8 · PP=4 · DP=2',18,'middle');
  for(let row=0;row<4;row++) {
    const y=85+row*92;
    for(let col=0;col<2;col++) node(off+20+col*210,y,row+4*col,kind==='A'?'전체 층':`${row*8+1}–${row*8+8}층`);
    arrow(off+177,y+31,off+223,y+31,true);
    if(row<3) for(let col=0;col<2;col++) arrow(off+95+210*col,y+68,off+95+210*col,y+86,kind==='A');
  }
  text(off+200,460,kind==='A'?'8개 노드가 서로 다른 배치':'열 하나가 모델 복제본 하나',18,'middle',ink,true);
  text(off+200,487,kind==='A'?'DP: 같은 G 번호의 8개 GPU':'점선 DP: 같은 행·같은 G 번호',17,'middle');
  text(off+200,512,kind==='A'?'각 노드 안에서 모든 층을 TP로 계산':'실선 PP: 아래로 activation 전달',17,'middle');
}
p.push(`<path d="M400 15 V522" stroke="${line}"/>`);
text(400,546,'작은 칸 = GPU G0–G7 · 각 노드 안의 8개 GPU가 TP 통신',18,'middle');
save('week02-parallel-layout.svg');

// 각 행의 8칸은 같은 파라미터 구간이다. 용량에 비례한 막대가 아니다.
start(485,'DP와 ZeRO 단계별로 GPU가 보관하는 가중치 gradient optimizer 상태');
text(400,29,'같은 8개 GPU에서 무엇을 나누어 저장할까?',22,'middle',ink,true);
text(400,57,'W: 가중치 · G: gradient · O: master weight + Adam 상태',18,'middle');
for(let stage=0;stage<4;stage++) {
  const x=stage*200;
  text(x+100,94,['DP','ZeRO-1','ZeRO-2','ZeRO-3'][stage],21,'middle',ink,true);
  for(let gpu=0;gpu<2;gpu++) {
    const y=120+gpu*132;
    text(x+100,y,`N0:G${gpu}`,18,'middle');
    ['W','G','O'].forEach((key,r)=>{
      text(x+17,y+29+r*31,key,18);
      for(let shard=0;shard<8;shard++) {
        const sharded = stage >= [3,2,1][r];
        rect(x+40+shard*18,y+12+r*31,16,23,(!sharded || shard===gpu)?ink:'white',line,1);
      }
    });
  }
  text(x+100,384,'G2–G7도 같은 규칙',16,'middle',mid);
  text(x+100,420,[128,44,30,16][stage]+' GB / GPU',21,'middle',ink,true);
}
text(400,453,'진한 칸: 해당 GPU가 보관 · 빈 칸: 다른 GPU가 담당',18,'middle');
text(400,478,'칸은 파라미터 구간을 뜻하며 byte 크기에 비례하지 않는다.',17,'middle',mid);
save('week02-zero-shards.svg');

// 모든 forward를 마친 뒤 backward를 진행하는 flush schedule의 의존성을 지킨다.
start(380,'두 pipeline stage와 세 microbatch의 forward backward 시간표');
text(400,29,'PP=2 · microbatch A/B/C · optimizer step 1회',22,'middle',ink,true);
text(400,58,'모든 forward 후 backward하는 예 · 칸 하나는 같은 계산 시간',18,'middle');
const rows=[['F_A','F_B','F_C','','','B_C','B_B','B_A'],['','F_A','F_B','F_C','B_C','B_B','B_A','']];
for(let k=0;k<8;k++) text(160+k*77+35,106,k+1,18,'middle');
text(20,105,'시간 →',18);
rows.forEach((row,r)=>{
  const y=128+r*92;
  text(20,y+26,`N${r} · TP=8`,18,'start',ink,true);
  text(20,y+51,r===0?'1–16층':'17–32층',18);
  row.forEach((v,k)=>{
    const back=v.startsWith('B');
    rect(160+k*77,y,70,65,back?ink:(v?'#e2e8f0':'white'),line);
    text(195+k*77,y+39,v.replace('_',' ')||'대기',18,'middle',back?'white':ink);
  });
});
text(400,327,'F: forward (N0 → N1) · B: backward (N1 → N0)',18,'middle');
text(400,356,'빈 구간이 bubble · 모든 backward가 끝난 뒤 한 번 갱신',18,'middle');
save('week02-pipeline-timeline.svg');

start(670,'두 독립 문서를 함께 저장한 입력 정답 위치 번호 loss mask와 attention mask');
text(400,28,'같은 배열에 저장해도 문서별 문맥과 정답은 유지',22,'middle',ink,true);
const cellsX=180, cw=78;
text(cellsX+cw*1.5,65,'문서 A',20,'middle',ink,true);
text(cellsX+cw*5,65,'문서 B',20,'middle',ink,true);
const data=[['입력',['BOS','부산','항구','BOS','코드','실행','완료']],['정답',['부산','항구','EOS','코드','실행','완료','EOS']],['Position ID',[0,1,2,0,1,2,3]],['Loss mask',[1,1,1,1,1,1,1]]];
data.forEach(([label,values],r)=>{
  const y=82+r*43;
  text(24,y+27,label,18);
  values.forEach((v,i)=>{rect(cellsX+i*cw,y,cw-4,36,i<3?'#e2e8f0':pale,line,2);text(cellsX+i*cw+(cw-4)/2,y+25,v,18,'middle');});
});
text(400,289,'Attention mask: 행의 query가 열의 key를 볼 수 있는가?',19,'middle',ink,true);
const labels=['A0','A1','A2','B0','B1','B2','B3'], ax=245, ay=337, ac=40;
labels.forEach((v,i)=>{text(ax+i*ac+18,ay-13,v,17,'middle');text(ax-15,ay+i*ac+25,v,17,'end');});
for(let i=0;i<7;i++) for(let j=0;j<7;j++) {
  const allow=j<=i && (i<3)===(j<3);
  rect(ax+j*ac,ay+i*ac,36,36,allow?ink:'white',line,0);
  if(allow) text(ax+j*ac+18,ay+i*ac+25,'1',17,'middle','white');
}
rect(580,362,22,22,ink); text(612,380,'참조 허용',18);
rect(580,401,22,22,'white'); text(612,419,'참조 차단',18);
text(580,470,'B는 A를 읽지 않는다.',18);
text(580,501,'Loss mask와',18);
text(580,528,'attention mask는',18);
text(580,555,'별도 설정이다.',18);
text(400,649,'Position ID를 다시 시작하는 것만으로 문서 간 attention이 차단되지는 않는다.',17,'middle',mid);
save('week02-packed-documents.svg');
