function setInnerHTML(elm, html) {
  elm.innerHTML = html;
  
  Array.from(elm.querySelectorAll("script"))
    .forEach( oldScriptEl => {
      const newScriptEl = document.createElement("script");
      
      Array.from(oldScriptEl.attributes).forEach( attr => {
        newScriptEl.setAttribute(attr.name, attr.value) 
      });
      
      const scriptText = document.createTextNode(oldScriptEl.innerHTML);
      newScriptEl.appendChild(scriptText);
      
      oldScriptEl.parentNode.replaceChild(newScriptEl, oldScriptEl);
  });
};

function getScreenSize(option) {
  let testRequest = new Request('http://localhost:' + option['port'] +'/function/js_result_save', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json;charset=utf-8;',
          'Access-Control-Allow-Origin':'*',
          'Access-Control-Allow-Credentials': 'true',
          'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'
        },
        body: JSON.stringify({'js_func_input':{'height': screen.height, 'width': screen.width},
                              'event_id': 'screen_size'})
      });
      fetch(testRequest).then(response => {});
  return 
}
