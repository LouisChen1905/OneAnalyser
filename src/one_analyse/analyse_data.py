#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年3月26日

@author: chensi
'''

from one_analyse.lib.db.ormtables import OneORM
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
from sqlalchemy.orm.session import sessionmaker
from one_analyse import one_engine
from sqlalchemy.sql.schema import Table
from sqlalchemy.util.langhelpers import symbol

DBSession = sessionmaker(bind=one_engine)


if __name__ == '__main__':
    db2 = OneORM() 
    db2.InitDB()
    
    
#     print(db.select_period())
#     periods = db2.get_periods()
#     for period in periods:
#         print(period)
        
    # plot
    session = DBSession()
#     period_rows = db2.get_periods_cost(session)
    
    period_cost_max = db2.get_periods_max_cost(session)
    period_cost = [row.cost for row in period_cost_max]
    period_max_cost = [row.max_num for row in period_cost_max]
    period_cost_x = range(1, len(period_cost_max)+1)
    session.commit()
#     print(period_cost_x)
#     print(period_cost_y)
    
    trace0 = go.Scatter(
                       y = period_cost,
                       name = 'win cost',
                       mode = 'markers',
                       marker = dict(
                                     symbol = 'diamond'
                                     )
                       )
    trace1 = go.Scatter(
                        y = period_max_cost,
                        name = 'max cost',
                        mode = 'markers',
                        marker = dict(
                                      symbol = 'x'
                                      )
                    )
    data0 = [trace0, trace1]
    
    plot(data0, filename='cost-line.html')
    
    # cost section filter
    step = 1
    cost_section = list(range(step,7000,step))
    period_count = [x[0][0] for x in db2.count_periods_const(session, cost_section)]
#     print(period_count)
    trace1 = go.Bar(
                    y = period_count)
    data1 = [trace1]
    plot(data1, filename = 'cost_count.html')

    session.close()