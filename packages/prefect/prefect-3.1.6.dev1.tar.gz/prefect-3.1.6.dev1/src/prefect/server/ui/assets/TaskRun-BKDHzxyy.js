import{d as C,W as F,v as O,e as s,ao as V,bx as j,bK as f,bL as B,c as i,g as a,a as c,h as p,u as P,aO as W,o as k,j as n,k as e,bM as H,bN as _,A as J,y as R,bO as K,t as M,D as Q,bP as U,bQ as X,bI as Z,a6 as $,bo as q}from"./index-BSYHczDy.js";import{u as z}from"./usePageTitle-DXMrnpL1.js";const tt=C({__name:"TaskRun",setup(E){const g=P(),d=F("taskRunId"),v=O(),m=s(()=>[{label:"Details",hidden:W.xl},{label:"Logs"},{label:"Artifacts"},{label:"Task Inputs"}]),l=V("tab","Logs"),{tabs:w}=j(m,l),I=s(()=>d.value?[d.value]:null),y=f(v.taskRuns.getTaskRun,I,{interval:3e4}),t=s(()=>y.response),r=s(()=>{var u;return(u=t.value)==null?void 0:u.flowRunId}),h=s(()=>r.value?[r.value]:null),T=f(v.flowRuns.getFlowRun,h),b=s(()=>{var u;return(u=t.value)!=null&&u.taskInputs?JSON.stringify(t.value.taskInputs,void 0,2):"{}"});function x(){T.refresh(),g.push(q.flowRun(r.value))}B(t);const D=s(()=>t.value?`Task Run: ${t.value.name}`:"Task Run");return z(D),(u,o)=>{const N=p("p-code-highlight"),A=p("p-tabs"),L=p("p-layout-well");return t.value?(k(),i(L,{key:0,class:"task-run"},{header:a(()=>[n(e(H),{"task-run-id":t.value.id,onDelete:x},null,8,["task-run-id"])]),well:a(()=>[n(e(_),{alternate:"","task-run":t.value},null,8,["task-run"])]),default:a(()=>[n(A,{selected:e(l),"onUpdate:selected":o[0]||(o[0]=S=>$(l)?l.value=S:null),tabs:e(w)},J({details:a(()=>[n(e(_),{"task-run":t.value},null,8,["task-run"])]),logs:a(()=>[n(e(U),{"task-run":t.value},null,8,["task-run"])]),artifacts:a(()=>[t.value?(k(),i(e(X),{key:0,"task-run":t.value},null,8,["task-run"])):c("",!0)]),"task-inputs":a(()=>[t.value?(k(),i(e(Z),{key:0,"text-to-copy":b.value},{default:a(()=>[n(N,{lang:"json",text:b.value,class:"task-run__inputs"},null,8,["text"])]),_:1},8,["text-to-copy"])):c("",!0)]),_:2},[t.value?{name:"task-inputs-heading",fn:a(()=>[o[1]||(o[1]=R(" Task inputs ")),n(e(K),{title:"Task Inputs"},{default:a(()=>[R(M(e(Q).info.taskInput),1)]),_:1})]),key:"0"}:void 0]),1032,["selected","tabs"])]),_:1})):c("",!0)}}});export{tt as default};
//# sourceMappingURL=TaskRun-BKDHzxyy.js.map
