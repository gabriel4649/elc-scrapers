var urls= [];
for (var i= document.links.length; i-->0;)
    if (document.links[i].hostname===location.hostname)
        urls.push(document.links[i].href);

function copyToClipboard (text) {
    window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);
}

copyToClipboard(urls)
