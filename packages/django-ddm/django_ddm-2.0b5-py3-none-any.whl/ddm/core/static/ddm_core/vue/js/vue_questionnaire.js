(function(){"use strict";var e={9859:function(e,t,n){var s=n(3864);const i=["data-page-index"],r={key:0,class:"question-container"},o=["id"],a={key:1,class:"question-container"},u=["id"],d={key:2,class:"question-container"},l=["id"],c={key:3,class:"question-container"},h=["id"],p={key:4,class:"question-container"},m=["id"],q={key:5,class:"question-container"},g=["id"],f={class:"row flow-navigation"},v={class:"col"};function b(e,t,n,b,C,k){const L=(0,s.g2)("SingleChoiceQuestion"),y=(0,s.g2)("MultiChoiceQuestion"),x=(0,s.g2)("OpenQuestion"),E=(0,s.g2)("MatrixQuestion"),T=(0,s.g2)("SemanticDifferential"),M=(0,s.g2)("TransitionQuestion");return(0,s.uX)(),(0,s.CE)(s.FK,null,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(C.parsedQuestConfig,(t=>(0,s.bo)(((0,s.uX)(),(0,s.CE)("div",{key:t.question,"data-page-index":t.page},["single_choice"===t.type?((0,s.uX)(),(0,s.CE)("div",r,[(0,s.bF)(L,{qid:t.question,text:t.text,items:t.items,onResponseChanged:k.updateResponses,class:"question-body"},null,8,["qid","text","items","onResponseChanged"]),(0,s.Lk)("div",{id:"required-hint-"+t.question,class:"required-hint hidden"},(0,s.v_)(e.$t("required-but-missing-hint")),9,o)])):(0,s.Q3)("",!0),"multi_choice"===t.type?((0,s.uX)(),(0,s.CE)("div",a,[(0,s.bF)(y,{qid:t.question,text:t.text,items:t.items,required:t.required,onResponseChanged:k.updateResponses,class:"question-body"},null,8,["qid","text","items","required","onResponseChanged"]),(0,s.Lk)("div",{id:"required-hint-"+t.question,class:"required-hint hidden"},(0,s.v_)(e.$t("required-but-missing-hint")),9,u)])):(0,s.Q3)("",!0),"open"===t.type?((0,s.uX)(),(0,s.CE)("div",d,[(0,s.bF)(x,{qid:t.question,text:t.text,options:t.options,onResponseChanged:k.updateResponses,class:"question-body"},null,8,["qid","text","options","onResponseChanged"]),(0,s.Lk)("div",{id:"required-hint-"+t.question,class:"required-hint hidden"},(0,s.v_)(e.$t("required-but-missing-hint")),9,l)])):(0,s.Q3)("",!0),"matrix"===t.type?((0,s.uX)(),(0,s.CE)("div",c,[(0,s.bF)(E,{qid:t.question,text:t.text,items:t.items,scale:t.scale,onResponseChanged:k.updateResponses,class:"question-body"},null,8,["qid","text","items","scale","onResponseChanged"]),(0,s.Lk)("div",{id:"required-hint-"+t.question,class:"required-hint hidden"},(0,s.v_)(e.$t("required-but-missing-hint")),9,h)])):(0,s.Q3)("",!0),"semantic_diff"===t.type?((0,s.uX)(),(0,s.CE)("div",p,[(0,s.bF)(T,{qid:t.question,text:t.text,items:t.items,scale:t.scale,onResponseChanged:k.updateResponses,class:"question-body"},null,8,["qid","text","items","scale","onResponseChanged"]),(0,s.Lk)("div",{id:"required-hint-"+t.question,class:"required-hint hidden"},(0,s.v_)(e.$t("required-but-missing-hint")),9,m)])):(0,s.Q3)("",!0),"transition"===t.type?((0,s.uX)(),(0,s.CE)("div",q,[(0,s.bF)(M,{qid:t.question,text:t.text,onResponseChanged:k.updateResponses,class:"question-body"},null,8,["qid","text","onResponseChanged"]),(0,s.Lk)("div",{id:"required-hint-"+t.question,class:"required-hint hidden"},(0,s.v_)(e.$t("required-but-missing-hint")),9,g)])):(0,s.Q3)("",!0)],8,i)),[[s.aG,C.currentPage===t.page]]))),128)),(0,s.Lk)("div",f,[(0,s.Lk)("div",v,[(0,s.Lk)("button",{class:"flow-btn",type:"button",onClick:t[0]||(t[0]=e=>(k.next(),k.scrollToTop()))},(0,s.v_)(e.$t("next-btn-label"))+"  ›",1)])])],64)}n(4114),n(7642),n(8004),n(3853),n(5876),n(2475),n(5024),n(1698),n(8992),n(3949);const C=["innerHTML"],k=["id"],L={class:"form-check-label rb-cb-label"},y=["dataid","name","value"],x=["innerHTML"];function E(e,t,n,i,r,o){return(0,s.uX)(),(0,s.CE)("div",null,[(0,s.Lk)("div",{innerHTML:n.text},null,8,C),(0,s.Lk)("div",{id:"answer-"+n.qid,class:"question-response-body"},[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.items,((e,i)=>((0,s.uX)(),(0,s.CE)("div",{key:i,class:"question-choice-item form-check"},[(0,s.Lk)("label",L,[(0,s.Lk)("input",{class:"form-check-input",type:"radio",dataid:n.qid,name:"q-"+n.qid,value:e.value,onChange:t[0]||(t[0]=e=>o.responseChanged(e))},null,40,y),(0,s.Lk)("span",{innerHTML:e.label},null,8,x)])])))),128))],8,k)])}var T={name:"SingleChoiceQuestion",props:["qid","text","items"],emits:["responseChanged"],data:function(){return{response:""}},created(){this.response=-99,this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})},methods:{responseChanged(e){this.response=e.target.value,this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})}}},M=n(6262);const X=(0,M.A)(T,[["render",E]]);var H=X;const w=["innerHTML"],Q={class:"question-response-body"},_={class:"form-check-label rb-cb-label"},R=["name","value"],S=["innerHTML"];function P(e,t,n,i,r,o){return(0,s.uX)(),(0,s.CE)("div",null,[(0,s.Lk)("div",{innerHTML:n.text},null,8,w),(0,s.Lk)("div",Q,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.items,((e,n)=>((0,s.uX)(),(0,s.CE)("div",{key:n,class:"question-choice-item form-check"},[(0,s.Lk)("label",_,[(0,s.Lk)("input",{class:"form-check-input",type:"checkbox",name:e.id,value:e.value,onChange:t[0]||(t[0]=e=>o.responseChanged(e))},null,40,R),(0,s.Lk)("span",{innerHTML:e.label},null,8,S)])])))),128))])])}var $={name:"MultiChoiceQuestion",props:["qid","text","items"],emits:["responseChanged"],data:function(){return{response:{}}},created(){this.items.forEach((e=>{this.response[e.id]=!1})),this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})},methods:{responseChanged(e){this.response[e.target.name]=e.target.checked,this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})}}};const O=(0,M.A)($,[["render",P]]);var F=O;const A=["innerHTML"],I=["id"],j=["name"],K=["name"];function D(e,t,n,i,r,o){return(0,s.uX)(),(0,s.CE)("div",null,[(0,s.Lk)("div",{innerHTML:n.text},null,8,A),(0,s.Lk)("div",{id:"answer-"+n.qid,class:"question-response-body"},["small"==n.options.display?((0,s.uX)(),(0,s.CE)("input",{key:0,type:"text",name:n.qid,onChange:t[0]||(t[0]=e=>o.responseChanged(e))},null,40,j)):(0,s.Q3)("",!0),"large"==n.options.display?((0,s.uX)(),(0,s.CE)("textarea",{key:1,class:"open-question-textarea",type:"text",name:n.qid,onChange:t[1]||(t[1]=e=>o.responseChanged(e))},null,40,K)):(0,s.Q3)("",!0)],8,I)])}var z={name:"OpenQuestion",props:["qid","text","options"],emits:["responseChanged"],data:function(){return{response:"-99"}},created(){this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:null})},methods:{responseChanged(e){this.response=e.target.value,this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:null})}}};const B=(0,M.A)(z,[["render",D]]);var N=B;const U=["innerHTML"],J={class:"mq-table"},G={class:"mq-header"},W=(0,s.Lk)("th",null,null,-1),V=["innerHTML"],Y=["id"],Z=["innerHTML"],ee=["name","value"],te=["innerHTML"];function ne(e,t,n,i,r,o){return(0,s.uX)(),(0,s.CE)("div",null,[(0,s.Lk)("div",{innerHTML:n.text},null,8,U),(0,s.Lk)("table",J,[(0,s.Lk)("thead",G,[(0,s.Lk)("tr",null,[W,((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.scale,((e,t)=>((0,s.uX)(),(0,s.CE)("th",{key:t,innerHTML:e.label},null,8,V)))),128))])]),(0,s.Lk)("tbody",null,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.items,((e,i)=>((0,s.uX)(),(0,s.CE)("tr",{key:i,id:"answer-item-"+e.id},[(0,s.Lk)("td",{class:"mq-table-td-item",innerHTML:e.label},null,8,Z),((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.scale,((n,i)=>((0,s.uX)(),(0,s.CE)("td",{key:i,class:(0,s.C4)(["mq-table-td-input",{"border-start":n.add_border,"border-secondary":n.add_border}])},[(0,s.Lk)("label",null,[(0,s.Lk)("input",{type:"radio",name:e.id,value:n.value,onChange:t[0]||(t[0]=e=>o.responseChanged(e))},null,40,ee),(0,s.Lk)("span",{class:"ps-2 d-sm-none",innerHTML:n.label},null,8,te)])],2)))),128))],8,Y)))),128))])])])}var se={name:"MatrixQuestion",props:["qid","text","items","scale"],emits:["responseChanged"],data:function(){return{response:{}}},created(){this.items.forEach((e=>{this.response[e.id]=-99})),this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})},methods:{responseChanged(e){this.response[e.target.name]=e.target.value,this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})}}};const ie=(0,M.A)(se,[["render",ne]]);var re=ie;const oe=["innerHTML"],ae={class:"question-response-body"},ue={class:"dq-table"},de=(0,s.Lk)("th",null,null,-1),le=["innerHTML"],ce=(0,s.Lk)("th",null,null,-1),he=["id"],pe=["innerHTML"],me=["name","value"],qe=["innerHTML"];function ge(e,t,n,i,r,o){return(0,s.uX)(),(0,s.CE)("div",null,[(0,s.Lk)("div",{innerHTML:n.text},null,8,oe),(0,s.Lk)("div",ae,[(0,s.Lk)("table",ue,[(0,s.Lk)("thead",null,[(0,s.Lk)("tr",null,[de,((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.scale,((e,t)=>((0,s.uX)(),(0,s.CE)("th",{key:t,innerHTML:e.label},null,8,le)))),128)),ce])]),(0,s.Lk)("tbody",null,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.items,((e,i)=>((0,s.uX)(),(0,s.CE)("tr",{key:i,id:"answer-item-"+e.id},[(0,s.Lk)("td",{class:"mq-table-td-item dq-table-td-item-left",innerHTML:e.label},null,8,pe),((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(n.scale,((n,i)=>((0,s.uX)(),(0,s.CE)("td",{key:i,class:"dq-table-td-input"},[(0,s.Lk)("label",null,[(0,s.Lk)("input",{type:"radio",name:e.id,value:n.value,onChange:t[0]||(t[0]=e=>o.responseChanged(e))},null,40,me)])])))),128)),(0,s.Lk)("td",{class:"mq-table-td-item dq-table-td-item-right",innerHTML:e.label_alt},null,8,qe)],8,he)))),128))])])])])}var fe={name:"SemanticDifferential",props:["qid","text","items","scale"],emits:["responseChanged"],data:function(){return{response:{}}},created(){this.items.forEach((e=>{this.response[e.id]=-99})),this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})},methods:{responseChanged(e){this.response[e.target.name]=e.target.value,this.$emit("responseChanged",{id:this.qid,response:this.response,question:this.text,items:this.items})}}};const ve=(0,M.A)(fe,[["render",ge]]);var be=ve;const Ce=["innerHTML"];function ke(e,t,n,i,r,o){return(0,s.uX)(),(0,s.CE)("div",null,[(0,s.Lk)("div",{innerHTML:n.text},null,8,Ce)])}var Le={name:"TransitionQuestion",props:["qid","text"],emits:["responseChanged"],created(){this.$emit("responseChanged",{id:this.qid,response:null,question:this.text,items:null})}};const ye=(0,M.A)(Le,[["render",ke]]);var xe=ye,Ee={name:"QApp",components:{SingleChoiceQuestion:H,MultiChoiceQuestion:F,OpenQuestion:N,MatrixQuestion:re,SemanticDifferential:be,TransitionQuestion:xe},props:{questionnaireConfig:String,actionUrl:String,language:String},data(){return this.$i18n.locale=this.language,{parsedQuestConfig:JSON.parse(this.questionnaireConfig),responses:{},currentPage:1,minPage:1,maxPage:1,locale:this.language,displayedRequiredHint:!1}},created(){this.setMaxPage(),this.currentPage=this.minPage},watch:{locale(e){this.$i18n.locale=e}},methods:{scrollToTop(){this.$nextTick((()=>{setTimeout((()=>{document.documentElement.scrollTo({top:0,behavior:"smooth"}),document.documentElement.scrollTop=0,document.body.scrollTop=0}),100)}))},updateResponses(e){this.responses[e.id]={response:e.response,question:e.question,items:e.items}},setMaxPage(){let e=[];this.parsedQuestConfig.forEach((t=>e.push(t.page))),this.minPage=Math.min(...e),this.maxPage=Math.max(...e)},next(){(this.displayedRequiredHint||this.checkRequired())&&(this.currentPage===this.maxPage?this.submitData():(this.currentPage+=1,null===document.querySelector("[data-page-index='"+this.currentPage+"']")&&this.next()))},getActiveQuestions(){let e=[];return this.parsedQuestConfig.forEach((t=>{this.currentPage===t.page&&e.push(t)})),e},checkRequired(){let e=[],t=new Set;return this.getActiveQuestions().forEach((n=>{if(document.querySelectorAll("div[id*=answer-], tr[id*=answer-]").forEach((e=>e.classList.remove("required-but-missing"))),document.querySelectorAll("div[class*=required-hint]").forEach((e=>e.classList.remove("show"))),n.required){let s=this.responses[n.question].response;if(s instanceof Object)for(let i in s)-99!==s[i]&&"-99"!==s[i]||(e.push("item-"+i),t.add(n.question));else-99!==s&&"-99"!==s||(e.push(n.question),t.add(n.question))}})),0===e.length||(e.forEach((e=>{let t="answer-"+e;document.getElementById(t).classList.add("required-but-missing")})),t.forEach((e=>{document.getElementById("required-hint-"+e).classList.add("show")})),this.displayedRequiredHint=!0,!1)},submitData(){let e=new FormData;e.append("post_data",JSON.stringify(this.responses));let t=document.querySelector("input[name='csrfmiddlewaretoken']");e.append("csrfmiddlewaretoken",t.value),fetch(this.actionUrl,{method:"POST",body:e}).then((e=>{e.redirected&&(window.location.href=e.url)})).catch((e=>{console.info(e)}))}}};function Te(e){e.__i18n=e.__i18n||[],e.__i18n.push({locale:"",resource:{en:{"next-btn-label":e=>{const{normalize:t}=e;return t(["Next"])},"required-but-missing-hint":e=>{const{normalize:t}=e;return t(["Please answer this question."])}},de:{"next-btn-label":e=>{const{normalize:t}=e;return t(["Weiter"])},"required-but-missing-hint":e=>{const{normalize:t}=e;return t(["Bitte beantworten Sie diese Frage."])}}}})}"function"===typeof Te&&Te(Ee);const Me=(0,M.A)(Ee,[["render",b]]);var Xe=Me,He=n(6992);const we=new He.hU({fallbackLocale:"en"}),Qe="#qapp",_e=document.querySelector(Qe),Re=(0,s.Ef)(Xe,{..._e.dataset});Re.use(we),Re.mount(Qe)}},t={};function n(s){var i=t[s];if(void 0!==i)return i.exports;var r=t[s]={exports:{}};return e[s].call(r.exports,r,r.exports,n),r.exports}n.m=e,function(){var e=[];n.O=function(t,s,i,r){if(!s){var o=1/0;for(l=0;l<e.length;l++){s=e[l][0],i=e[l][1],r=e[l][2];for(var a=!0,u=0;u<s.length;u++)(!1&r||o>=r)&&Object.keys(n.O).every((function(e){return n.O[e](s[u])}))?s.splice(u--,1):(a=!1,r<o&&(o=r));if(a){e.splice(l--,1);var d=i();void 0!==d&&(t=d)}}return t}r=r||0;for(var l=e.length;l>0&&e[l-1][2]>r;l--)e[l]=e[l-1];e[l]=[s,i,r]}}(),function(){n.d=function(e,t){for(var s in t)n.o(t,s)&&!n.o(e,s)&&Object.defineProperty(e,s,{enumerable:!0,get:t[s]})}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.j=307}(),function(){var e={307:0};n.O.j=function(t){return 0===e[t]};var t=function(t,s){var i,r,o=s[0],a=s[1],u=s[2],d=0;if(o.some((function(t){return 0!==e[t]}))){for(i in a)n.o(a,i)&&(n.m[i]=a[i]);if(u)var l=u(n)}for(t&&t(s);d<o.length;d++)r=o[d],n.o(e,r)&&e[r]&&e[r][0](),e[r]=0;return n.O(l)},s=self["webpackChunkddm_vue_frontend"]=self["webpackChunkddm_vue_frontend"]||[];s.forEach(t.bind(null,0)),s.push=t.bind(null,s.push.bind(s))}();var s=n.O(void 0,[504],(function(){return n(9859)}));s=n.O(s)})();
//# sourceMappingURL=vue_questionnaire.js.map