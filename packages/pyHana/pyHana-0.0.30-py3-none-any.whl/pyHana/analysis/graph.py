import matplotlib.pyplot as plt
from . import findSignals as bs
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.gridspec import GridSpec

def CANDLE_CHART(ax, dfData
              , dfBuySellList = []
              , pType = '종가'
              , frPriceRatio = 0
              , toPriceRatio = 0
              , priceMAInd = True 
              , chart_type = 'C'        # 'C' : 캔들차트 / 'B' : 바차트
              , offset = 0.3            # bar차트 시가,종가 길이(0.1 ~ 0.5) 
              , line_width = 1          # bar차트 너비 크기 ( > 0.1) 
              , candle_width = 0.8      # 캔들차트 너비 크기 (0 ~ 1) 
              , chart_transparency = 0.3# 주가차트의 투명도 (0 ~ 1)                     
              , chart_height = 0.8      # 주가 차트의 최대 높이 비율 (0 ~ 1)
              , vol_height = 0.4        # 거래량 바차트의 최대 높이 비율 (0 ~ 1)   
              , vol_color = ''          # 거래량 바차트의 color
              , vol_transparency = 0.4  # 거래량 바차트의 투명도 (0 ~ 1) 
              , vol_width = 0.9         # 거래량 바차트의 너비 크기 (0 ~ 1)
              , signal_text_buy = 'B'
              , signal_text_sell= 'S'
              , signal_color_buy = 'black'
              , signal_color_sell = 'black'
              , signal_size = 20
              , signal_alpha = 1
               ):
    
    def create_candle(xcoord, open, high, low, close, candle_width):
        bottom_y = min([open, close])       # 시가가 종가 중 낮은 값이 박스 좌하단 y좌표
        bottom_x = xcoord - 0.5*candle_width # 박스 좌하단 x좌표
        bottom_left = (bottom_x, bottom_y)  # 박스 좌하단 좌표
        height = abs(close - open)          # 저가에서 고가를 나타내는 직선
 
        rect = Rectangle(bottom_left, candle_width, height) ## 박스 객체
        line = [(xcoord, low), (xcoord, high)] ## 선분 좌표 리스트
        return rect, line

    color_list = []    
    DATA_CNT = len(dfData)
    xcoords = range(DATA_CNT)
    if chart_type == '':
        chart_type = 'C'
         
    if chart_height > 0:
        if chart_type == 'C':
            rect_list = []
            line_list = []
            
        elif chart_type == 'B':
            line_width = max(0.1, line_width)
            OFFSET = max(0.1, min(offset, 0.5))
            lines = []
            openlines = []
            closelines = []
            
        ax.set_xlim(0, DATA_CNT - 1)

        for x, data in enumerate(dfData[['시가','고가','저가','종가']].reset_index(drop=True).values):
            open, high, low, close = data       
            color = 'r' if close >= open else 'b'
            color_list.append(color)            
            
            if chart_type == 'C':
                rect, line = create_candle(x, open, high, low, close, candle_width)
                rect_list.append(rect)
                line_list.append(line)
                
            elif chart_type == 'B':
                vline = Line2D( xdata=(x, x), ydata=(low, high), color=color, linewidth=line_width, antialiased=True)
                openline = Line2D(xdata=(x - OFFSET, x), ydata=(open,open),
                                  color=color, linewidth=line_width, antialiased=True)
                closeline = Line2D(xdata=(x , x + OFFSET), ydata=(close,close),
                                  color=color, linewidth=line_width, antialiased=True)     
                
                ax.add_line(vline)
                ax.add_line(openline)
                ax.add_line(closeline)                

        if chart_type == 'C':
            ## Rectanlge과 Line을 각각 PatchCollection과 LineCollection에 담아 collection에 추가
            ax.add_collection( LineCollection(line_list, edgecolor=color_list, linewidths=candle_width,
                                              alpha = chart_transparency) )
            ax.add_collection( PatchCollection(rect_list, facecolor=color_list, edgecolor=color_list, 
                                               match_original=True, alpha = chart_transparency) )
            
        elif chart_type == 'B':
            ax.autoscale_view()
                
        y_max = dfData['고가'].max()    
        y_min = dfData['저가'].min()        
        y_min = max (0, y_max - (y_max - y_min) / chart_height)
        if frPriceRatio > 0:            
            y_min = min(y_min, dfData['이동평균'+pType].min() * frPriceRatio )       
        
        ax.set_ylim(y_min, y_max)    
        
        # 이동평균선 표시
        if priceMAInd == True:
            ma5 = dfData[pType].rolling(window=5).mean()
            ax.plot(xcoords, ma5, label='MA5')
            ma20 = dfData[pType].rolling(window=20).mean()
            ax.plot(xcoords, ma20, label='MA20')
            ma60 = dfData[pType].rolling(window=60).mean()
            ax.plot(xcoords, ma60, label='MA60')

        if frPriceRatio > 0:            
            ax.plot(xcoords, dfData['이동평균'+pType] * frPriceRatio, label='MA(하한)')
        if toPriceRatio > 0:            
            ax.plot(xcoords, dfData['이동평균'+pType] * toPriceRatio, label='MA(상한)')        

        # 매수/매도 표시 
        if len(dfBuySellList) > 0:
            # for i, sign in enumerate(dfBuySellList):
            #     if sign == 'B':
            #         ax.plot(i, dfData[pType].iloc[i], '>', markersize=10, color='black')             
            #     elif sign == 'S':
            #         ax.plot(i, dfData[pType].iloc[i], '<', markersize=10, color='black')   

            # ax.plot(dfBuySellList['매수Idx'], dfBuySellList['매수가격'], '>', markersize=10, color='black')     
            # ax.plot(dfBuySellList['매도Idx'], dfBuySellList['매도가격'], '<', markersize=10, color='black')          
            for i in range(len(dfBuySellList)):
                # ax.text(dfBuySellList['매수Idx'].iloc[i], dfBuySellList['매수가격'].iloc[i], signal_text_buy, 
                #         size=signal_size, color=signal_color_buy, weight='bold', alpha=signal_alpha, horizontalalignment='center', verticalalignment='center')
                # ax.text(dfBuySellList['매도Idx'].iloc[i], dfBuySellList['매도가격'].iloc[i], signal_text_sell, 
                #         size=signal_size, color=signal_color_sell, weight='bold', alpha=signal_alpha, horizontalalignment='center', verticalalignment='center')                      

                ax.annotate(signal_text_buy, (dfBuySellList['매수Idx'].iloc[i], dfBuySellList['매수가격'].iloc[i]), # 텍스트를 출력할 좌표
                            ha='center', va='center', # 정렬
                            fontsize = signal_size, color=signal_color_buy, weight='bold', alpha=signal_alpha )    
                ax.annotate(signal_text_sell, (dfBuySellList['매도Idx'].iloc[i], dfBuySellList['매도가격'].iloc[i]), # 텍스트를 출력할 좌표
                            ha='center', va='center', # 정렬
                            fontsize = signal_size, color=signal_color_sell, weight='bold', alpha=signal_alpha )      


    # 2) 거래량 바 차트
    if vol_height > 0:
               
        ax2 = ax.twinx()
        ax2.set_ylim(0, dfData['거래량'].max() / vol_height ) 
            # vol_height : 주가 데이터가 가려지는걸 방지하기 위해, 거래량 bar의 최대 크기 조절
        
        if vol_color == '':
            vol_color = color_list 
        ax2.bar(xcoords, dfData['거래량'], color = vol_color, alpha = vol_transparency, width=vol_width)
        ax2.set_yticks([x for x in ax2.get_yticks()]) 
        ax2.set_yticklabels(['{:.0f}'.format(x) for x in ax2.get_yticks()])   
    
    if DATA_CNT > 50:
        tick_skip_cnt = int(DATA_CNT/50)        
    else:
        tick_skip_cnt = 1

    xList = dfData['일자'].to_list()
    ax.set_xticks( list(range(0, DATA_CNT, tick_skip_cnt)) , 
                  [xList[i] for i in xcoords if i%tick_skip_cnt == 0], 
                  rotation=90)    
    
    ax.legend(loc='upper left')
    ax.set_xmargin(0.01) ## 좌우 여백 비율
    ax.set_ymargin(0.01) ## 위아래 여백 비율    

def MACD_CHART(ax, macd):

    data_cnt = len(macd)
    if data_cnt > 0:
        xcoords = range(data_cnt)
        
        # 1) MACD
        ax.set_xlim(0, data_cnt - 1)
        ax.set_title('MACD',fontsize=15)
        ax.plot(xcoords, macd['signal'], label='MACD Signal')
        ax.plot(xcoords, macd['macd'], label='MACD')

        ax.xaxis.set_visible(False)

        # 2) MACD 오실레이터
        ax2 = ax.twinx()
    #     ax2.set_title('MACD Oscillator',fontsize=15)        
        ax2.bar(list(xcoords),list(macd['diff'].where(macd['diff'] < 0)), 0.7)
        ax2.bar(list(xcoords),list(macd['diff'].where(macd['diff'] > 0)), 0.7) # 0.7 bar 두께
        ax.legend(loc='upper left')


def VOLUME_CHART(ax, dfData
              , dfBuySellList = []
              , vol_color = ''          # 거래량 바차트의 color
              , vol_transparency = 0    # 거래량 바차트의 투명도 (0 ~ 1) 
              , vol_width = 0.9         # 거래량 바차트의 너비 크기 (0 ~ 1)
              , vol_type = '거래량'
              , vol_ratio_fr = 2
              , signal_text_buy = 'B'
              , signal_text_sell= 'S'
              , signal_color_buy = 'black'
              , signal_color_sell = 'black'
              , signal_size = 20
              , signal_alpha = 1              
               ):
    
    color_list = []    
    DATA_CNT = len(dfData)
    xcoords = range(DATA_CNT)
    
    ax.set_xlim(0, DATA_CNT - 1)

    for data in dfData[['시가','고가','저가','종가']].reset_index().values:
        x, open, high, low, close = data        
        color = 'r' if close >= open else 'b'
        color_list.append(color)            
            
    y_max = dfData[vol_type].max()    
    y_min = dfData[vol_type].min()                
    ax.set_ylim(y_min, y_max)    
        
    # 이동평균선 표시
    # ma60 = dfData[vol_type].rolling(window=60).mean()
    ax.plot(xcoords, dfData['이동평균'+vol_type], label='이동평균'+vol_type)
    ax.plot(xcoords, dfData['이동평균'+vol_type] * vol_ratio_fr, label='이동평균(최소배수)')
    ax.legend(loc='upper left')

    # 매수/매도 표시 
    if len(dfBuySellList) > 0:
        # y_list = [y_min for i in range(len(dfBuySellList))]
        # ax.plot(dfBuySellList['매수Idx'], y_list, '>', markersize=10, color='black')             
        # ax.plot(dfBuySellList['매도Idx'], y_list, '<', markersize=10, color='black')          
        for i in range(len(dfBuySellList)):  
            # ax.text(dfBuySellList['매수Idx'].iloc[i], 0, signal_text_buy, 
            #         size=signal_size, color=signal_color_buy, weight='bold', alpha=signal_alpha, horizontalalignment='center', verticalalignment='bottom')
            # ax.text(dfBuySellList['매도Idx'].iloc[i], 0, signal_text_sell, 
            #         size=signal_size, color=signal_color_sell, weight='bold', alpha=signal_alpha, horizontalalignment='center', verticalalignment='bottom')                      
            
            ax.annotate(signal_text_buy, (dfBuySellList['매수Idx'].iloc[i], dfBuySellList['매수가격'].iloc[i]), # 텍스트를 출력할 좌표
                        ha='center', va='center', # 정렬
                        fontsize = signal_size, color=signal_color_buy, weight='bold', alpha=signal_alpha )    
            ax.annotate(signal_text_sell, (dfBuySellList['매도Idx'].iloc[i], dfBuySellList['매도가격'].iloc[i]), # 텍스트를 출력할 좌표
                        ha='center', va='center', # 정렬
                        fontsize = signal_size, color=signal_color_sell, weight='bold', alpha=signal_alpha )      



    if vol_color == '':
        vol_color = color_list 
    ax.bar(xcoords, dfData['거래량'], color = vol_color, alpha = vol_transparency, width=vol_width)
    ax.set_yticks([x for x in ax.get_yticks()]) 
    ax.set_yticklabels(['{:.0f}'.format(x) for x in ax.get_yticks()])   
    
    # if DATA_CNT > 50:
    #     tick_skip_cnt = int(DATA_CNT/50)        
    # else:
    #     tick_skip_cnt = 1

    # xList = dfData['일자'].to_list()
    # ax.set_xticks( list(range(0, DATA_CNT, tick_skip_cnt)) , 
    #               [xList[i] for i in xcoords if i%tick_skip_cnt == 0], 
    #               rotation=90)    
            
    ax.set_xmargin(0.01) ## 좌우 여백 비율
    ax.set_ymargin(0.01) ## 위아래 여백 비율    

def INDEX_CHART(ax, dfData, mIndexNm):
    data_cnt = len(dfData)
    if data_cnt > 0:
        xcoords = range(data_cnt)
        
        # 1) 마켓 지수 
        ax.set_xlim(0, data_cnt - 1)
        ax.set_title(mIndexNm, fontsize=15)
        ax.plot(xcoords, dfData[mIndexNm], label=mIndexNm, color='red')
        ax.xaxis.set_visible(False)

        # 2) 마켓 지수 오실레이터
        ax2 = ax.twinx()
        ax2.bar(list(xcoords),list(dfData['diff'].where(dfData['diff'] < 0)), 0.7)        
        ax2.bar(list(xcoords),list(dfData['diff'].where(dfData['diff'] > 0)), 0.7) # 0.7 bar 두께
        
        ax.legend(loc='upper left')
        ax.set_xmargin(0.01) ## 좌우 여백 비율
        ax.set_ymargin(0.01) ## 위아래 여백 비율    
    
def draw_candle_market_index(df
                   , title=''
                   , titleSize = 25
                   , dfBuySellList = []
#                    , pType = '종가'
                   , chart_type = ''
                   , offset = 0.3 
                   , line_width = 1
                   , candle_width = 0.8
                   , chart_transparency = 0.3
                   , chart_height = 0.8
                   , vol_height = 0.4
                   , vol_color = ''
                   , vol_transparency = 0.4
                   , vol_width = 0.9
                   , mIndexNm = ''
                   , signal_text_buy = 'B'
                   , signal_text_sell= 'S'
                   , signal_color_buy = 'black'
                   , signal_color_sell = 'black'
                   , signal_size = 20          
                   , signal_alpha = 1         
                    ):

    fig = plt.figure(figsize=(100, 60))
    fig.set_facecolor('white')
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 font 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False     # minus font 깨짐 방지

    gs = GridSpec(nrows=2, ncols=1, height_ratios=(5, 2))

    # 1) 일별 주가 그리기
    ax = fig.add_subplot(gs[0, 0])
    ax.set_title(title, fontsize=titleSize)
    
    CANDLE_CHART(
                 ax
               , df 
               , dfBuySellList = dfBuySellList          # 매수, 매도 표시
#                , pType = pType                # '시가', '종가'
               , chart_type = chart_type      # 'C' : 캔들차트 / 'B' : 바차트
               , offset = offset              # 바차트 시가,종가 길이(0.1 ~ 0.5) 
               , line_width = line_width      # 바차트 너비 범위( > 0.1)             
               , candle_width = candle_width  # 캔들차트 너비 범위(0.1 ~ 1) 
               , chart_transparency = chart_transparency  # 주가차트의 투명도 (0 ~ 1) 
               , chart_height = chart_height  # 주가차트의 최대 높이 비율 (0 ~ 1)     
               , vol_height = vol_height      # 거래량 바차트의 최대 높이 비율 (0 ~ 1)
               , vol_color = vol_color        # 거래량 바차트의 color
               , vol_transparency = vol_transparency # 거래량 바차트의 투명도 (0 ~ 1) 
               , vol_width = vol_width        # 거래량 바차트의 너비 범위 (0 ~ 1)         
               , signal_text_buy = signal_text_buy
               , signal_text_sell= signal_text_sell
               , signal_color_buy = signal_color_buy
               , signal_color_sell = signal_color_sell
               , signal_size = signal_size          
               , signal_alpha = signal_alpha     
               )

    ax2 = fig.add_subplot(gs[1, 0])
    INDEX_CHART(ax2, df, mIndexNm)

    plt.show()

def draw_candle_macd(df
                   , title=''
                   , titleSize = 25
                   , dfBuySellList = []
                   , pType = '종가'
                   , chart_type = ''
                   , offset = 0.3 
                   , line_width = 1
                   , candle_width = 0.8
                   , chart_transparency = 0.3
                   , chart_height = 0.8
                   , vol_height = 0.4
                   , vol_color = ''
                   , vol_transparency = 0.4
                   , vol_width = 0.9
                   , macd = []
                   , signal_text_buy = 'B'
                   , signal_text_sell= 'S'
                   , signal_color_buy = 'black'
                   , signal_color_sell = 'black'
                   , signal_size = 20          
                   , signal_alpha = 1         
                    ):

    fig = plt.figure(figsize=(100, 60))
    fig.set_facecolor('white')
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 font 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False     # minus font 깨짐 방지

    gs = GridSpec(nrows=2, ncols=1, height_ratios=(5, 2))

    # 1) 일별 주가 그리기
    ax = fig.add_subplot(gs[0, 0])
    ax.set_title(title, fontsize=titleSize)
    
    CANDLE_CHART(
                 ax
               , df 
               , dfBuySellList = dfBuySellList          # 매수, 매도 표시
               , pType = pType                # '시가', '종가'
               , chart_type = chart_type      # 'C' : 캔들차트 / 'B' : 바차트
               , offset = offset              # 바차트 시가,종가 길이(0.1 ~ 0.5) 
               , line_width = line_width      # 바차트 너비 범위( > 0.1)             
               , candle_width = candle_width  # 캔들차트 너비 범위(0.1 ~ 1) 
               , chart_transparency = chart_transparency  # 주가차트의 투명도 (0 ~ 1) 
               , chart_height = chart_height  # 주가차트의 최대 높이 비율 (0 ~ 1)     
               , vol_height = vol_height      # 거래량 바차트의 최대 높이 비율 (0 ~ 1)
               , vol_color = vol_color        # 거래량 바차트의 color
               , vol_transparency = vol_transparency # 거래량 바차트의 투명도 (0 ~ 1) 
               , vol_width = vol_width        # 거래량 바차트의 너비 범위 (0 ~ 1)         
               , signal_text_buy = signal_text_buy
               , signal_text_sell= signal_text_sell
               , signal_color_buy = signal_color_buy
               , signal_color_sell = signal_color_sell
               , signal_size = signal_size          
               , signal_alpha = signal_alpha     
               )

    ax2 = fig.add_subplot(gs[1, 0])
    MACD_CHART(ax2, macd)

    plt.show()


def draw_candle_volume(df
                   , title=''
                   , titleSize = 25
                   , dfBuySellList = []
                   , pType = '종가'
                   , frPriceRatio = 0
                   , toPriceRatio = 0
                   , priceMAInd = True
                   , chart_type = 'C'
                   , offset = 0.3 
                   , line_width = 1
                   , candle_width = 0.8
                   , chart_transparency = 1
                   , chart_height = 1
                   , vol_color = ''
                   , vol_transparency = 1
                   , vol_width = 0.9
                   , vol_type = '거래량'
                   , signal_text_buy = 'B'
                   , signal_text_sell= 'S'
                   , signal_color_buy = 'black'
                   , signal_color_sell = 'black'
                   , signal_size = 20     
                   , signal_alpha = 1         
                   , vol_ratio_fr = 2            
                    ):

    fig = plt.figure(figsize=(100, 60))
    fig.set_facecolor('white')
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 font 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False     # minus font 깨짐 방지

    gs = GridSpec(nrows=2, ncols=1, height_ratios=(4, 3))

    # 1) 일별 주가 그리기
    ax = fig.add_subplot(gs[0, 0])
    ax.set_title(title, fontsize=titleSize)
    
    CANDLE_CHART(
                 ax
               , df 
               , dfBuySellList = dfBuySellList          # 매수, 매도 표시
               , pType = pType                # '시가', '종가'
               , frPriceRatio = frPriceRatio
               , toPriceRatio = toPriceRatio
               , priceMAInd = priceMAInd      # 5일, 20일, 60일 이동평균선 표시 여부 (defualt = True)
               , chart_type = chart_type      # 'C' : 캔들차트 / 'B' : 바차트
               , offset = offset              # 바차트 시가,종가 길이(0.1 ~ 0.5) 
               , line_width = line_width      # 바차트 너비 범위( > 0.1)             
               , candle_width = candle_width  # 캔들차트 너비 범위(0.1 ~ 1) 
               , chart_transparency = chart_transparency  # 주가차트의 투명도 (0 ~ 1) 
               , chart_height = chart_height  # 주가차트의 최대 높이 비율 (0 ~ 1)           
               , vol_height = 0               # 거래량 바차트의 최대 높이 비율 (0 ~ 1)   
               , signal_text_buy = signal_text_buy
               , signal_text_sell= signal_text_sell
               , signal_color_buy = signal_color_buy
               , signal_color_sell = signal_color_sell
               , signal_size = signal_size     
               , signal_alpha = signal_alpha                
               )

    ax2 = fig.add_subplot(gs[1, 0])
    VOLUME_CHART(ax2
               , df
               , dfBuySellList = dfBuySellList
               , vol_color = vol_color        # 거래량 바차트의 color
               , vol_transparency = vol_transparency # 거래량 바차트의 투명도 (0 ~ 1) 
               , vol_width = vol_width        # 거래량 바차트의 너비 범위 (0 ~ 1)      
               , vol_type = vol_type          
               , signal_text_buy = signal_text_buy
               , signal_text_sell= signal_text_sell
               , signal_color_buy = signal_color_buy
               , signal_color_sell = signal_color_sell
               , signal_size = signal_size          
               , signal_alpha = signal_alpha    
               , vol_ratio_fr = vol_ratio_fr                 
               )

    plt.show()    