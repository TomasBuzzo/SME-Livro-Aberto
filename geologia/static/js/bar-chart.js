window.addEventListener('load', function(){
    let barchart = d3.selectAll('table.bar-chart');
    barchart.selectAll('tr')
        .style('cursor', 'pointer')
        .on('click', function(){
            d3.select(this).select('a').dispatch('click');
        });
    barchart.selectAll('a')
        .on('click', function(){
            const target = new URL(this.href)
            const selection = d3.select(this.hash);
            d3.select(selection.node().parentNode)
                .select('.card.active')
                .classed('active', false);
            selection.classed('active', true);
            d3.event.preventDefault();
            d3.event.stopPropagation();
        });
})
