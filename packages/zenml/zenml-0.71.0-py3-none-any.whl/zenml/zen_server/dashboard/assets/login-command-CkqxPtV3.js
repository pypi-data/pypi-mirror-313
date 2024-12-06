function o(n){switch(n){case"local":return"zenml login --local";case"docker":return"zenml login --local --docker";default:return`zenml login ${window.location.origin}`}}export{o as g};
