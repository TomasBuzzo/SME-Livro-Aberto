let style =  el => window.getComputedStyle(el);
let margin = (name, el) => parseFloat(style(el)['margin' + name]) || 0;
let px = n => parseFloat(n) + 'px';

function height(el){
    let baseHeight = el.getClientRects()[0].height
    let margins = margin('Top', el) + margin('Bottom', el);
    return baseHeight + margins;
}

function byLabel(a, b) {
    let nameA = a.dataset.label.toUpperCase();
    let nameB = b.dataset.label.toUpperCase();
    if (nameA < nameB) { return -1; }
    if (nameA > nameB) { return 1;  }
    return 0;
}

function byValue(a, b) {
    return b.dataset.value - a.dataset.value;
}

window.addEventListener("DOMContentLoaded", function(){
    let barsEl = document.querySelectorAll('#localidade .barchart > .bar');
    let bars = Array.prototype.slice.call(barsEl);
    let ys = bars.map((bar, i) => height(bar) * i);

    let style = document.createElement('style');
    style.type = 'text/css';
    let rule = (y, i) => `.localidade-bar-${i}{ transform: translateY(${px(y)}); }`;
    let rules = ys.map(rule);
    style.innerHTML = rules.join('\n');
    document.getElementsByTagName('head')[0].appendChild(style);

    let barchart = document.querySelector('#localidade .barchart');
    barchart.style.position = 'relative';
    barchart.style.height = px(height(bars[0]) + ys[ys.length - 1]);

    function sortOnChange(){
        let sortFunc = this.checked? byLabel : byValue;
        bars.sort(sortFunc)
        bars.forEach((bar, i) => {
            bar.style.position = 'absolute';
            bar.className = `bar localidade-bar-${i}`;
        });

    }

    let localidadeOrderSwitch = document.querySelector('#localidade-order');
    localidadeOrderSwitch.addEventListener('change', sortOnChange);
    sortOnChange.call(localidadeOrderSwitch)
});

let baseUrl = '/static/regionalizacao/maps/'

window.addEventListener("DOMContentLoaded", function(){
    var width = document.body.clientWidth,
        height = document.body.clientHeight;

    var svg = d3.select('svg.map-container')
        .attr('viewBox', '0 0 ' + width + ' ' + height);

    var gMap = svg.select('g.map');

    d3.json(baseUrl + 'distritos.topojson').then(function (data){
        let features = topojson.feature(data, data.objects.Distritos);

        projection = d3.geoMercator()
            .fitSize([width / 2, height], features)

        var path = d3.geoPath().projection(projection)
        function title(d){ return d.properties.NOME; }
        gMap.selectAll('path')
            .data(features.features)
            .enter()
            .append('path')
            .attr('d', path)
            .append('title')
            .text(title);
    });
});
