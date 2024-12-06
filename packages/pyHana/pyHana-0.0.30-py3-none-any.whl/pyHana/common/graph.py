import matplotlib.pyplot as plt

plt.rcParams['font.family'] ='Malgun Gothic'
# plt.rcParams['font.family'] ='NanumGothic'
plt.rcParams['axes.unicode_minus'] =False

title_font = {
    'fontsize': 14,
    'fontweight': 'bold'
}

colors = ['r','darkgoldenrod','tab:blue','tab:orange','silver','tab:gray',
        'tab:green','tab:purple','darkslateblue','black','tab:brown','tab:olive','tab:cyan',
        'gold','indianred','chocolate','tab:red','royalblue','lavender','lime','darkorange',
        'tan','g','b','y','m','c','k','forestgreen','brown'
        ]

def show_graph(xlabels, xValues1, xValues2, label1, label2):

    fig = plt.Figure()
    fig.clear()
    fig.set_tight_layout(True)
    plt.style.use('ggplot')

    fig = plt.figure(figsize=(20,10))
    fig.set_facecolor('lightsteelblue')        
    
    ax = fig.add_subplot(111)    
    ax2 = ax.twinx()
    
#     ax.set_ylim(1000, 3000)    
    ax.plot(xlabels, xValues1, color='black', label=label1, linewidth="1")
    ax2.plot(xlabels, xValues2, color='r', label=label2, linewidth="1")
    
    plt.xticks(ticks=xlabels, labels=xlabels, rotation=90)
    if len(xlabels) > 40:
            plt.locator_params(axis='x', nbins=40)          
            
    plt.title('거래Simulation', fontdict=title_font, loc='center', pad = 5)   

    plt.legend()
    plt.show()  

# def show_graph(xValues, yValues1, yValues2):

#     fig = plt.Figure()
#     fig.clear()
#     ax = fig.add_subplot(111)

#         self.fig.set_tight_layout(True)
#             ax2 = ax.twinx()

#             # 중간에 빈 데이터로 인해 그래프가 깨지는 현상 방지를 위해 plot 처리
#             ax2.plot(xlabels, xValues, color='g', linewidth="1")


#     plt.style.use('ggplot')

#     fig = plt.figure(figsize=(20,30))
#     fig.set_facecolor('lightsteelblue')    
    
#     plt.subplot(211)
#     plt.plot(xValues[colCond], xValues["value"], color='grey', linewidth="1")
#     plt.xticks(ticks=xValues[colCond], labels=xlabels, rotation=90)
#     if len(xlabels) > 40:
#             plt.locator_params(axis='x', nbins=40)        
#     plt.title(title1, fontdict=title_font, loc='center', pad = 5)        

#     plt.subplot(212)
#     plt.plot(xValues[colCond], xValues["value"], color='grey', linewidth="1")
#     plt.xticks(ticks=xValues[colCond], labels=xlabels, rotation=90)
#     if len(xlabels) > 40:
#         plt.locator_params(axis='x', nbins=40)       
#     plt.title(title2, fontdict=title_font, loc='center', pad = 5)    
    
#     yMax = 0          
#     yMin = 9999999     
    

#     for idx, x in enumerate(analObjList):                     
#         labelNm = (lambda x: x[3] if len(x[3])>0 else (x[2] if len(x[2])>0 else (x[1] if len(x[1])>0 else (x[0] if len(x[0])>0 else '전국'))))(x)        
#         objData = analObjData[analObjData['No']==idx]
#         color = colors[idx % len(colors)]
#         linestyle = (lambda x: '--' if x >= 10 else '-')(idx)
                  
#         plt.subplot(211)
#         if len(objData[colCond]) > 0:
#             plt.plot(objData[colCond], objData[colName211], label=labelNm, color=color, linestyle=linestyle) # , marker=x[4]
        
#         plt.subplot(212)
#         if len(objData[colCond][1:]) > 0:                  
#             plt.plot(objData[colCond][1:], objData[colName212][1:], label=labelNm, color=color, linestyle=linestyle) # , marker=x[4]      
        
#         if len(objData[colName211]) > 0:
#             yMax = max(yMax, max(objData[colName211]))  
#             yMin = min(yMin, min(objData[colName211]))  

#     if graphKnd == 'T2':
#         plt.subplot(211)
#         x = analObjList[0]                  

#         rowCond = 1
#         if  len(x[0]) > 0:
#             rowCond = rowCond & (dfRowData['시도'] == x[0]) 
#             if  len(x[1]) > 0:
#                 rowCond = rowCond & (dfRowData['시군구'] == x[1]) 
#                 if  len(x[2]) > 0:
#                     rowCond = rowCond & (dfRowData['법정동'] == x[2])
#                     if  len(x[3]) > 0:
#                         rowCond = rowCond & (dfRowData['아파트'] == x[3])
                        
#         if  x[4] == '2':  ## "1.전체, 2.면적(㎡)범위, 3.특정면적(㎡)
#             rowCond = rowCond & (dfRowData['면적'] == x[5])     
#             # print('x[5] > ', x[5])           #delete
#         elif  x[4] == '3':     
#             rowCond = rowCond & (dfRowData['전용면적_내림'] == int(x[5]))      
#             # print('x[5] > ', int(x[5]))           #delete             

#         dfRowData = dfRowData[rowCond]

#         if len(dfRowData[colCond]) > 0:
#             plt.plot(dfRowData[colCond], dfRowData['거래금액'], 'bo') # , marker=x[4]3


#     yMax *= 1.05
#     yMin *= 0.95
#     plt.subplot(211)    
#     plt.ylim(yMin, yMax)
#     plt.legend()
#     plt.subplot(212)    
#     plt.legend()

#     plt.show()  