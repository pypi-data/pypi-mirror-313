import{d as f,v as i,b as _,e as o,c as s,g as n,h as v,o as t,j as w,k as a,bR as b,q as k,bS as C,bT as h,F as y,a as x}from"./index-BSYHczDy.js";import{u as F}from"./usePageTitle-DXMrnpL1.js";const S=f({__name:"Flows",setup(g){const c=i(),l={interval:3e4},e=_(c.flows.getFlowsCount,[{}],l),r=o(()=>e.response??0),u=o(()=>e.executed&&r.value===0),p=o(()=>e.executed),m=()=>{e.refresh()};return F("Flows"),(B,D)=>{const d=v("p-layout-default");return t(),s(d,{class:"flows"},{header:n(()=>[w(a(b))]),default:n(()=>[p.value?(t(),k(y,{key:0},[u.value?(t(),s(a(C),{key:0})):(t(),s(a(h),{key:1,selectable:"",onDelete:m}))],64)):x("",!0)]),_:1})}}});export{S as default};
//# sourceMappingURL=Flows-DzWc-l3N.js.map
