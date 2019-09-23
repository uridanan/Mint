import dash_table


class Column:
    id = None
    name = None
    edit = False
    width = None
    align = 'left'

    def __init__(self, id, name, edit=False, align='left', width=None):
        self.id = id
        self.name = name
        self.edit = edit
        self.align = align
        self.width = width

    def toDict(self):
        return {'id': self.id, 'name': self.name, 'editable': self.edit}

    def style(self):
        if self.width is None:
            style = {'if': {'column_id': self.id}, 'textAlign': self.align}
        else:
            style = {'if': {'column_id': self.id}, 'textAlign': self.align, 'width': self.width}
        return style


class myDataTable:
    id = None
    df = None
    data = None
    columns = None
    sort = 'none'
    filter = 'none'
    listView = True
    selectRows = False
    selectedRows = []
    maxRows = 200

    def __init__(self, id, df, cols=None):
        self.id = id
        self.df = df
        self.initData()
        if cols is None:
            self.initColumns()
        else:
            self.setColumns(cols)

    def initData(self):
        self.data = self.getData(self.df,self.maxRows)

    @staticmethod
    def getData(dataframe, max_rows=200):
        return [
            dict(entry=i, **{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]

    def initColumns(self):
        #self.columns = [{'id': p, 'name': p} for p in self.df.columns[1:]]
        self.columns = [Column(p,p) for p in self.df.columns[1:]]

    def setColumns(self, cols):
        self.columns = cols

    def getColumns(self):
        return [c.toDict() for c in self.columns]

    def getColumnStyles(self):
        return [c.style() for c in self.columns]

    def enableSort(self):
        self.sort = 'native'

    def enableFilter(self):
        self.filter = 'native'

    def setSelectRows(self,selected):
        self.selectRows = 'multi'
        self.selectedRows = selected

    def showGrid(self):
        self.listView = False

    def setMaxRows(self, max):
        self.maxRows = max

    def generate(self):
        return dash_table.DataTable(
            id=self.id,
            # Header
            columns=self.getColumns(),
            # Body
            #data=[],
            data=self.data,
            sort_action=self.sort,
            filter_action=self.filter,
            editable=False,
            row_selectable=self.selectRows,
            selected_rows=self.selectedRows,
            style_as_list_view=self.listView,

            style_table={
                #'overflowY': 'scroll',
                #'maxHeight': '600',
                #'maxWidth': '1500',
                '--accent':'#78daf1',
                '--hover': '#d6fbff',
                '--selected-row': '#d6fbff',
                '--selected-background': '#d6fbff'
            },
            style_cell={
                'whiteSpace': 'normal',
                'text-align': 'left',
                'hover': 'hotpink'
            },
            style_header={
                'whiteSpace': 'normal',
                'background-color': '#555',
                'color': 'white',
                'font-weight': 'bold',
                'height': '50px',
                'textAlign': 'left'
            },
            style_data={
                'accent': '#78daf1',
                'hover': '#d6fbff'
            },

            #style_filter=self.getColumnStyles(),
            style_header_conditional=self.getColumnStyles(),
            style_filter_conditional=self.getColumnStyles(),
            style_cell_conditional=self.getColumnStyles(),

            #Alternate row colors
            style_data_conditional=[
                #{'if': {'row_index': i}, 'backgroundColor': '#3D9970', 'color': 'white'} for i in selected_rows
                {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(255,255,255)'},
                {'if': {'row_index': 'even'}, 'backgroundColor': 'rgb(242, 254, 255)'}
            ]
        )




