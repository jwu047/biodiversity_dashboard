// Takes in sample and builds metadata, builds gaugeplot
function buildMetadata(sample) {
    // D3 send http request to REST API to load .json and returns parsed json object
    d3.json(`/metadata/${sample}`).then((data) => {
        // D3 select panel
        var PANEL = d3.select("#sample-metadata");

        // clear existing 
        PANEL.html("");

        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries
        // Adds key, value pair to the panel
        Object.entries(data).forEach(([key, value]) => {
            // D3 append method for each new pair
            PANEL.append("h6").text(`${key}: ${value}`);
        });

        // Build gauge chart using wfreq from 'data' passed in
        buildGauge(data.WFREQ);
    });
}

function buildCharts(sample) {
    d3.json(`/samples/${sample}`).then((data) => {
        const otu_ids = data.otu_ids;
        const otu_labels = data.otu_labels;
        const sample_values = data.sample_values;

        // Bubble Chart 
        // https://plotly.com/javascript/bubble-charts/
        var bubbleData = [{
            x: otu_ids,
            y: sample_values,
            name: `Sample ${sample}`,
            text: otu_labels,
            mode: "markers",
            marker: {
                size: sample_values,
                color: otu_ids
            }
        }];
        var bubbleLayout = {
            margin: { t: 0 },
            hovermode: "closest",
            xaxis: { title: "OTU ID" }
        };

        // Plot on div with id "bubble"
        Plotly.plot("bubble", bubbleData, bubbleLayout);


        // Pie Chart with 10 slices
        var pieData = [{
            values: sample_values.slice(0, 10),
            labels: otu_ids.slice(0, 10),
            hovertext: otu_labels.slice(0, 10),
            hoverinfo: "hovertext",
            textposition: "inside",
            type: "pie"
        }];
        var pieLayout = {
            margin: { t: 0, l: 0 }
        };

        // Plot on div with id "pie"
        Plotly.plot("pie", pieData, pieLayout);
    });
}

// Initial page load
function init() {
    // Select element
    var selector = d3.select("#selDataset");

    // Populate select options from list of sample names in REST API /names
    d3.json("/names").then((sampleNames) => {
        sampleNames.forEach((sample) => {
            // create select element with options that have the property attribute and text as 'sample'
            selector.append("option")
                .text(sample)
                .property("value", sample);
        });

        // Initialize page with first sample
        const firstSample = sampleNames[0];
        buildCharts(firstSample);
        buildMetadata(firstSample);
    });
}

// Changes charts with this.value as argument
function optionChanged(newSample) {
    // removes current traces to only show new one
    Plotly.deleteTraces("bubble", 0);
    buildCharts(newSample);
    buildMetadata(newSample);
}


//  Initialize by invoking/calling init();
init();