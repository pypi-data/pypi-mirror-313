import{d as v,v as g,b as y,e as s,c as n,g as i,h as r,o as a,j as l,k as o,cB as k,y as N,q as x,cC as C,cD as B,F as b,a as T}from"./index-BSYHczDy.js";import{u as V}from"./usePageTitle-DXMrnpL1.js";const I=v({__name:"Notifications",setup(h){const u=g(),t=y(u.notifications.getNotifications),c=s(()=>t.response??[]),f=s(()=>t.executed&&c.value.length===0),p=s(()=>t.executed);return V("Notifications"),(w,e)=>{const d=r("p-message"),m=r("p-layout-default");return a(),n(m,{class:"notifications"},{header:i(()=>[l(o(k))]),default:i(()=>[l(d,{info:""},{default:i(()=>e[2]||(e[2]=[N(" Notifications are deprecated and will be migrated in the future. Please use Automations. ")])),_:1}),p.value?(a(),x(b,{key:0},[f.value?(a(),n(o(C),{key:0})):(a(),n(o(B),{key:1,notifications:c.value,onDelete:e[0]||(e[0]=_=>o(t).refresh()),onUpdate:e[1]||(e[1]=_=>o(t).refresh())},null,8,["notifications"]))],64)):T("",!0)]),_:1})}}});export{I as default};
//# sourceMappingURL=Notifications-w0fv_Dcu.js.map
