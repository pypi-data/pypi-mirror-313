"use strict";(self.webpackChunk_atoti_jupyterlab_extension=self.webpackChunk_atoti_jupyterlab_extension||[]).push([[1327],{91327:(e,t,n)=>{n.r(t),n.d(t,{default:()=>u});var r=n(74389),a=n(40570),i=n(90923),o=n(31529),c=n(93345),s=n(36289);const u=e=>{const t=(0,c.useRef)(null),n=(0,c.useRef)(null),u=(0,c.useRef)(null),[l,p]=(0,c.useState)(0),d=(0,o.isArray)(e.disabled)&&!e.disabled[1];return(0,c.useEffect)((()=>{if(d){const e=Array.from(t.current?.querySelectorAll(".ant-picker-input > input")??[]);n.current=e[0],u.current=e[1];const r=()=>p(0);n.current?.addEventListener("focus",r);const a=()=>p(1);return u.current?.addEventListener("focus",a),()=>{n.current?.removeEventListener("focus",r),u.current?.removeEventListener("focus",a)}}return p(0),()=>{}}),[d]),(0,r.Y)("div",{"aria-label":"Date picker",ref:t,css:a.css`
        position: relative;
        .ant-picker-active-bar {
          opacity: 1;
        }
        .ant-picker-dropdown {
          left: 0% !important;
          top: 32px !important;
          opacity: 1 !important;
          transform: scale(1) !important;
        }
      `,children:(0,r.Y)(i.ConfigProvider,{theme:{components:{DatePicker:{boxShadowSecondary:"unset",motionDurationMid:"unset",sizePopupArrow:0}}},children:(0,r.Y)(s.DateRangePicker,{...e,open:!0,onCalendarChange:(...t)=>{if(d){const e=(l+1)%2;p(e),(0===e?n:u).current?.focus()}e.onCalendarChange?.(...t)},activePickerIndex:l,getPopupContainer:e=>t.current??e,panelRender:e=>(0,r.FD)("div",{css:{display:"flex",flexDirection:"column"},children:[e,(0,r.Y)(s.LegendForDatesWithData,{style:{alignSelf:"flex-end"}})]})})})})}}}]);