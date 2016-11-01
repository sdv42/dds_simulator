#!/usr/bin/env python3
def put_html_to_file(file_name, page):
    f  = open('%s.html' % file_name, 'w')
    f.write(page)
    f.close()

def make_html_chart(items_list, horizontal_axis_label, vertical_axis_label):
    html_page_header = '''
<html>
    <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load('visualization', '1', { packages : ['controls'] } );
            google.setOnLoadCallback(createTable);

            function createTable() {
                var myData = new google.visualization.DataTable();
                myData.addColumn('number', '%s');
                myData.addColumn('number', '%s');
                myData.addRows([ '''
    chart_item = '''
                [%f, %f], '''
    html_page_foter = '''                 
                ]);
                var dash_container = document.getElementById('dashboard_div'),
                    myDashboard = new google.visualization.Dashboard(dash_container);

                var myDateSlider = new google.visualization.ControlWrapper({
                    'controlType':'ChartRangeFilter',
                    'containerId':'control_div',
                    'options': {
                        'filterColumnLabel':'%s',
                    }
                });

                var myLine = new google.visualization.ChartWrapper({
                    'chartType':'AreaChart',
                    'containerId':'line_div',
                    'options': {
                        'theme':'maximized',
                    }
                });
                myDashboard.bind(myDateSlider, myLine );
                myDashboard.draw(myData);
            }
        </script>
    </head>
    <body>
        <div id="dashboard_div" style="height: 100%%;">
            <div id="control_div" style="height: 15%%;"></div>
            <div id="line_div"    style="height: 85%%;"></div>
        </div>
    </body>
</html> '''

    html_chart = html_page_header % (horizontal_axis_label, vertical_axis_label)
    for x, y in items_list:
        html_chart += chart_item % (x, y)
    html_chart += html_page_foter % horizontal_axis_label
    return html_chart

#TODO: fold copy paste to make_html_chartN function
def make_html_chart2(items_list, horizontal_axis_label, vertical_axis_label1, vertical_axis_label2):
    html_page_header = '''
<html>
    <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load('visualization', '1', { packages : ['controls'] } );
            google.setOnLoadCallback(createTable);

            function createTable() {
                var myData = new google.visualization.DataTable();
                myData.addColumn('number', '%s');
                myData.addColumn('number', '%s');
                myData.addColumn('number', '%s');
                myData.addRows([ '''
    chart_item = '''
                [%f, %f, %f], '''
    html_page_foter = '''                 
                ]);
                var dash_container = document.getElementById('dashboard_div'),
                    myDashboard = new google.visualization.Dashboard(dash_container);

                var myDateSlider = new google.visualization.ControlWrapper({
                    'controlType':'ChartRangeFilter',
                    'containerId':'control_div',
                    'options': {
                        'filterColumnLabel':'%s',
                    }
                });

                var myLine = new google.visualization.ChartWrapper({
                    'chartType':'AreaChart',
                    'containerId':'line_div',
                    'options': {
                        'theme':'maximized',
                    }
                });
                myDashboard.bind(myDateSlider, myLine );
                myDashboard.draw(myData);
            }
        </script>
    </head>
    <body>
        <div id="dashboard_div" style="height: 100%%;">
            <div id="control_div" style="height: 15%%;"></div>
            <div id="line_div"    style="height: 85%%;"></div>
        </div>
    </body>
</html> '''

    html_chart = html_page_header % (horizontal_axis_label, vertical_axis_label1, vertical_axis_label2)
    for x, a, b in items_list:
        html_chart += chart_item % (x, a, b)
    html_chart += html_page_foter % horizontal_axis_label
    return html_chart