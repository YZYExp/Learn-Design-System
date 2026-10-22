/** Runtime QA against actual native component preview iframes, not mock DOM.
 * Requires Playwright for this optional check and a native Tingly CLI.
 * DC_CHROME selects local Chrome; TINGLY_DESIGN_CLI selects cli.mjs.
 */
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const {chromium}=await import(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright/index.mjs' : 'playwright');
const base=path.dirname(fileURLToPath(import.meta.url));
const cli=process.env.TINGLY_DESIGN_CLI;
const cmd=cli?['node',cli]:['npx','--yes','tingly-design@0.26.1021'];
const proc=spawn(cmd[0],[...cmd.slice(1),'serve','--projects',base,'--port','0']);
let browser;
try{
 const port=await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>reject(Error('Native service readiness timed out')),30000);
  const rl=createInterface({input:proc.stdout});
  rl.on('line',s=>{if(s.includes('TINGLY_DESIGN_READY ')){clearTimeout(timer);rl.close();resolve(JSON.parse(s.split('TINGLY_DESIGN_READY ')[1]).port);}});
  proc.on('exit',c=>{clearTimeout(timer);reject(Error('Native service exited '+c));});
 });
 browser=await chromium.launch({...(process.env.DC_CHROME?{executablePath:process.env.DC_CHROME}:{}),headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1500,height:1200}});
 await page.goto('http://127.0.0.1:'+port+'/?p=refraction-system&v=components');
 await page.waitForTimeout(2500);
 const tab=page.getByRole('button',{name:'Components',exact:true});if(await tab.count())await tab.click();
 await page.waitForTimeout(1500);
 const results=[];
 for(const frame of page.frames().slice(1)){
  results.push(await frame.evaluate(()=>({text:document.body.innerText,namespace:typeof window.REFRACTION,images:[...document.images].map(x=>({src:x.getAttribute('src'),loaded:x.complete&&x.naturalWidth>0})),fontSize:document.querySelector('.title')?getComputedStyle(document.querySelector('.title')).fontSize:null})));
 }
 if(results.length!==3)throw Error('Expected three real native component preview iframes');
 if(results.some(r=>r.namespace!=='object'||r.images.some(x=>!x.loaded)))throw Error('Preview namespace or image failed');
 if(!results.some(r=>r.fontSize==='96px'))throw Error('Title typography did not consume native generated tokens');
 await fs.mkdir(base+'/refraction-system/renders',{recursive:true});
 await fs.writeFile(base+'/refraction-system/renders/component-live-qa.json',JSON.stringify({passed:true,results},null,2));
 console.log(JSON.stringify({passed:true,results},null,2));
}finally{if(browser)await browser.close();proc.kill('SIGTERM');}
