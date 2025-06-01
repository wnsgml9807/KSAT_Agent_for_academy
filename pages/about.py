import streamlit as st
import os
import streamlit_mermaid as stmd

# 현재 파일의 디렉토리를 기준으로 about.txt 경로 설정
file_path = os.path.join(os.path.dirname(__file__), "about.txt")
file_path4 = os.path.join(os.path.dirname(__file__), "image.png")
# about.txt 파일 읽기
try:
    with open(file_path, "r", encoding="utf-8") as f:
        about_text = f.read()
except FileNotFoundError:
    about_text = "오류: `about.txt` 파일을 찾을 수 없습니다. `frontend/pages/` 디렉토리에 파일을 생성해주세요."
except Exception as e:
    about_text = f"오류: 파일을 읽는 중 문제가 발생했습니다 - {e}"

st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap');
        .passage-font {
            border: 0.5px solid black;
            border-radius: 0px;
            padding: 10px;
            margin-bottom: 20px;
            font-family: 'Nanum Myeongjo', serif !important;
            line-height: 1.7;
            letter-spacing: -0.01em;
            font-weight: 500;
        }
        .passage-font p {
            text-indent: 1em; /* 각 문단의 첫 줄 들여쓰기 */
            margin-bottom: 0em;
        }
        .question-font {
            font-family: 'Nanum Myeongjo', serif !important;
            line-height: 1.7em;
            letter-spacing: -0.01em;
            font-weight: 500;
            margin-bottom: 1.5em;
        }
        /* <보기> 내 중첩 테이블 폰트 설정 */
        .question-font table tr td table {
            font-family: '돋움', Dotum, sans-serif !important; /* 돋움 폰트 적용, 없을 시 sans-serif */
            font-size: 0.95em; /* 기본 폰트보다 약간 작게 설정 (선택 사항) */
            line-height: 1.5em; /* 줄 간격 조정 (선택 사항) */
            font-weight: 500;
            letter-spacing: -0.02em;
        }
        </style>
        """, unsafe_allow_html=True)
    

# 파일에서 읽어온 내용 표시
st.info("왼쪽 사이드바에서 채팅으로 이동할 수 있습니다.")
st.write("""# KSAT Agent
_Multi-Agent 기반 수능 국어 독서 영역 출제 자동화 시스템_

```
제작자 : 권준희
소속 : 연세대학교 교육학과
ver 0.7.0 (06.01)
- 지문 작성용 Fine-tuned 모델 업그레이드
- 출제 절차 대폭 간소화 + 사용자 상호작용 강화
```

---

### 1️⃣ 개요

수능 국어, 특히 독서 지문의 출제에는 상당한 시간과 비용이 필요합니다.

KSAT Agent는 고품질의 수능 국어 독서 지문 세트를 **약 10분 안에** 완성하여 제공할 수 있습니다.

사용자는 AI와 함께 원하는 주제를 섬세하게 결정한 후, 나머지 출제 과정은 세 개의 AI 에이전트가 분담하여 처리합니다.

---

### 2️⃣ 효과성

- KSAT Agent 활용 시 기존 출제 프로세스를 크게 단축하고, 상당한 비용을 절감할 수 있습니다.

| 항목 (지문 당) | 기존  | KSAT Agent 사용 시 |
|------|---------|--------------------|
| **소요 시간** | 1 ~ 2 개월 | **10 분** |
| **비용** | 100~200만 원 | **200~500 원** (평균 사용량 기준) |
| **의사소통** | 서면 피드백 반복 | 수능 감각을 갖춘 AI와 **실시간 대화** |

---


### 3️⃣ 작업 흐름

1. 사용자가 원하는 분야와 주제를 선택하면, AI가 지문의 개요를 작성합니다.
2. 작성한 개요를 바탕으로, 전문 AI 에이전트가 지문을 작성합니다.
3. 지문 작성이 완료되면 전문 AI 에이전트가 문항을 출제합니다.
4. 사용자의 피드백 및 수정 과정을 거쳐 지문과 문항을 완성합니다.

---

### 4️⃣ 결과물 예시

*결과물은 일체 가공하지 않았습니다.*""")

gpt, ksat = st.columns(2, gap="large")

with gpt:
    st.write("""
    #### 일반 AI 결과물 (GPT 4.1)
    <div class="passage-font">
    <p>한 국가의 경제에서 환율 변동은 수출과 수입, 그리고 경상수지에 다양한 영향을 미친다. 특히 ‘J커브 현상’은 환율이 상승(자국 통화의 가치가 하락)할 때 경상수지의 변화 양상이 단순하지 않음을 보여주는 이론이다.</p>
    <p>예를 들어, 국내 기업들이 주로 원화로 비용을 지불하고, 수출 대금을 달러로 받는 한국 경제를 생각해 보자. 원/달러 환율이 상승하면, 달러로 표시된 상품 가격이 원화로 환산될 때 높아진다. 즉, 같은 달러 금액의 수출을 하더라도 이를 원화로 환산하면 더 많은 돈을 벌게 된다. 반면, 해외에서 수입하는 상품을 구매할 때는 더 많은 원화를 지불해야 한다.</p>
    <p>하지만 J커브 현상이 의미하는 바는 단순히 환율이 오르면 경상수지가 바로 개선되지 않는다는 점이다. 예를 들어, 한국의 한 해 수출액이 1,000억 달러, 수입액이 900억 달러라고 가정하자. 원/달러 환율이 1,000원에서 1,200원으로 20% 상승했다고 하더라도, 대부분의 수출·수입 계약은 미리 정해진 가격과 물량에 따라 진행된다. 환율이 급등한 직후에는 수입 원화 비용이 즉시 늘어나지만, 수출 물량이나 수입 물량은 단기적으로 거의 변하지 않는다. 이로 인해 수입 대금이 증가하면서 오히려 경상수지가 일시적으로 악화될 수 있다.</p>
    <p>시간이 지나면서 변화가 발생한다. 수입 상품의 가격이 오르면 소비자와 기업들은 대체재를 찾거나 수입을 줄이기 시작한다. 반면, 해외 시장에서는 한국 상품의 가격 경쟁력이 높아지기 때문에 수출 주문이 늘어난다. 대략 몇 개월에서 1년 정도의 시간이 흐르면, 수입은 감소하고 수출은 증가하여 경상수지가 점차 개선된다. 이 과정에서 경상수지의 변화 추이를 그래프로 나타내면, 처음에는 하락하다가 이후에 상승 곡선을 그리며 알파벳 ‘J’와 비슷한 형태가 나타난다.</p>
    <p>즉, J커브 현상은 환율 상승 → 단기적 경상수지 악화 → 중장기적 경상수지 개선이라는 순차적 과정을 설명한다. 이러한 현상은 단기에는 가격 효과(환율 변동에 따른 금액 증가)가, 장기에는 수량 효과(무역량 변화에 따른 효과)가 더 크게 작용하기 때문이다.</p>
    <p>따라서 J커브 현상은 환율정책을 운용할 때 정책 효과가 나타나는 시점과 그 원인을 이해하는 데 중요한 시사점을 제공한다.
    </div>

    <div class="question-font">
    [문항 1]  
    다음 중 J커브 현상에 대한 설명으로 적절하지 않은 것은?
    <br><br>
    <table>
        <tr>
            <td>ㄱ. 원/달러 환율이 상승할 경우, 경상수지는 즉시 개선된다.</td>
        </tr>
        <tr>
            <td>ㄴ. 단기적으로는 수입 대금이 증가해 경상수지가 악화될 수 있다.</td>
        </tr>
        <tr>
            <td>ㄷ. 시간이 지나면 수출은 증가하고 수입은 감소하여 경상수지가 개선될 수 있다.</td>
        </tr>
        <tr>
            <td>ㄹ. J커브라는 명칭은 경상수지의 변화 양상이 영문자 ‘J’와 유사하게 나타나기 때문이다.</td>
        </tr>
    </table>

    ① ㄱ  
    ② ㄴ  
    ③ ㄷ  
    ④ ㄹ  
    ⑤ ㄴ, ㄷ

    <hr style="margin:2em 0;">

    [문항 2]  
    J커브 현상에 대한 설명으로 가장 적절한 것을 고르시오.

    ① 환율 상승 직후에는 경상수지가 항상 개선된다.  
    ② 환율 상승이 장기적으로 경상수지 개선으로 이어지기까지는 무역량 변화가 필요하다.  
    ③ 모든 무역 계약은 환율 변동과 동시에 가격과 물량이 즉각 변동된다.  
    ④ 수입품 가격이 오르면 단기적으로 소비자와 기업의 행동 변화가 곧바로 일어난다.  
    ⑤ J커브 현상은 환율이 하락할 때만 나타난다.

    <hr style="margin:2em 0;">

    [문항 3]  
    다음 <보기>는 J커브 현상과 관련된 상황을 서술한 것이다. 이에 대한 이해로 가장 적절한 것을 고르시오.

    <보기>
    <table>
        <tr>
            <td>
                한 나라의 환율이 단기간에 15% 상승하였다. 이로 인해 수입품 가격이 즉각 오르면서, 해당 국가의 경상수지는 한동안 악화되는 모습을 보였다. 그러나 8개월이 지난 후부터 수출이 점차 늘어나고 수입이 감소하여 경상수지가 개선되기 시작하였다.  
                <br><br>
                경제학자 A는 이러한 현상이 국제무역 계약의 특성과 경제주체의 행동 변화가 시간이 지나면서 점진적으로 나타났기 때문이라고 설명하였다.
            </td>
        </tr>
    </table>
    </보기>

    ① 경상수지의 단기 악화는 환율 상승으로 인한 수입 대금 증가와 무역량의 즉각적 변화 때문이다.  
    ② J커브 현상에서는 환율이 상승한 직후부터 수출이 급격하게 증가한다.  
    ③ 환율 상승 직후, 대부분의 무역 계약은 이미 정해진 가격과 물량에 따라 이루어진다.  
    ④ 경제주체의 행동 변화는 환율 상승 직후 즉시 나타나 경상수지가 바로 개선된다.  
    ⑤ 장기적으로도 경상수지는 환율 변동과 관계없이 변하지 않는다.

    </div>

    

    """, unsafe_allow_html=True)

with ksat:
    st.write("""
    
    #### KSAT Agent 결과물 (전용 Fine-tuned AI 모델)          
             
    <div class="passage-font">
    <p>수출이 수입보다 많은 상태를 무역수지가 흑자라고 하고, 수입이 수출보다 많은 상태를 무역수지가 적자라고 한다. 환율은 자국 화폐와 외국 화폐의 교환 비율을 의미하는데, 일반적으로 환율이 상승하면 수출이 증가하고 수입이 감소하여 무역수지가 개선된다고 알려져 있다. 그런데 단기적으로는 무역수지가 오히려 악화되었다가 일정 기간이 지난 후에야 개선되는 현상이 나타나기도 한다. 이러한 현상을 J커브 효과라고 하는데, 그 이유는 무역수지의 변화 추이를 그래프로 나타내면 알파벳 J와 같은 모양이 되기 때문이다.</p>
    <p>그렇다면 J커브 효과는 왜 나타나는 것일까? 환율 변동에 따른 무역수지의 변화는 가격 효과와 물량 효과로 설명할 수 있다. 가격 효과란 환율 변동으로 인해 수출입 상품의 가격이 변동하여 무역수지가 변화하는 효과이고, 물량 효과란 가격 변동에 따라 수출입 상품의 물량이 변동하여 무역수지가 변화하는 효과이다. 환율이 상승하면 외국에서 보면 수출 상품의 가격은 이전보다 낮아지므로 수출은 증가하고, 수입 상품의 가격은 이전보다 높아지므로 수입은 감소하여 무역수지가 개선되는 것이 일반적인 경우이다.</p>
    <p>그런데 수출입 물량은 단기적으로는 변동하지 않는 경우가 많다. 이미 체결된 수출입 계약에 따라 일정 기간은 그 계약에서 정해진 물량이 거래되고, 그 이후에도 가격 변동에 따라 물량이 조정되는 데에는 시차가 존재하기 때문이다. 따라서 단기에는 가격 효과만 나타나게 된다. 환율이 상승하여 자국 화폐의 가치가 하락하면 동일한 양의 수입 상품을 수입하기 위해 지불해야 하는 자국 화폐의 액수는 증가한다. 즉, 수입 물량은 변하지 않지만 수입에 지출되는 자국 화폐의 액수는 증가한다. 한편, 수출 상품의 경우에는 자국 화폐로 지불되는 액수는 변하지 않는다. 이로 인해 단기에는 무역수지가 악화되는 현상이 나타나게 된다. 그러나 일정 기간이 지나고 나면 수출은 증가하고 수입은 감소하는 물량 효과가 나타나기 시작하여 무역수지가 개선되는 방향으로 전환된다.</p>
    <p>이러한 J커브 효과는 수출과 수입의 가격 탄력성이 중요한 역할을 한다. 가격 탄력성이란 상품의 가격이 변동할 때 그 가격 변동에 따라 수요나 공급이 민감하게 반응하는 정도를 말한다. 수출과 수입의 가격 탄력성이 크다면 환율 상승으로 인한 가격 변동에 따라 수출은 증가하고 수입은 감소하여 장기적으로는 무역수지가 개선되는 효과가 나타나게 된다.</p>
    </div>

    <div class="question-font">
    <b>3. ㉠ ‘가격 효과’와 ㉡ ‘물량 효과’에 대한 이해로 적절하지 <u>않은</u> 것은?</b><br>
    <div style="margin-left: 1em; margin-top: 7px;">
    <div style="text-indent: -1.5em; padding-left: 1.5em;">① 환율 상승 초기에는 ㉠이 주로 작용하여, 수입품에 대한 자국 화폐 지불액이 늘어나 무역수지가 악화될 수 있다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">② ㉡은 수출입 물량이 가격 변동에 반응하여 조정되는 것으로, 일반적으로 ㉠보다 시간적 지연을 두고 나타난다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">③ ㉠과 ㉡은 환율 변동이 무역수지에 미치는 영향을 설명하는 개념으로, J커브 효과의 발생 원인을 이해하는 데 기여한다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">④ 환율 상승 시 ㉠은 수출 상품의 외화 표시 가격을 하락시키고, ㉡은 수입 상품의 물량 감소를 유발하여 무역수지를 개선시킨다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">⑤ ㉠만 고려할 경우 환율 상승은 즉각적인 무역수지 개선을 가져오지만, ㉡의 지연된 발현으로 인해 J커브 현상이 나타난다.</div>
    </div>
    <br>
    
    <div class="question-font">
    <b>4. 다음 &lt;보기&gt;는 환율 상승 이후 시간에 따른 무역수지 변화를 나타낸 그래프이다. 윗글을 바탕으로 &lt;보기&gt;를 이해한 내용으로 적절하지 <u>않은</u> 것은? [3점]</b><br>
    <table style="margin-top: 7px; border: 1px solid #000; border-collapse: collapse; width: 100%;">
        <tr>
            <td style="text-align: center; font-weight: bold; background-color: #f8f8f8; padding: 5px;">
                &lt;보기&gt;
            </td>
        </tr>
        <tr>
            <td style="padding: 10px;">
                그래프는 T<sub>0</sub> 시점에서 환율이 상승한 이후 시간 경과에 따른 무역수지의 변화를 보여준다. 가로축은 시간, 세로축은 무역수지를 나타내며, 세로축의 0은 무역수지 균형 상태를 의미한다. T<sub>1</sub>은 무역수지가 최저점에 도달하는 시점, T<sub>2</sub>는 무역수지가 다시 균형 상태로 회복되는 시점, T<sub>3</sub> 이후는 무역수지가 개선되어 흑자 상태를 유지하는 시점이다.
                <svg width="400" height="250" viewBox="0 0 400 250" style="margin-top:10px; display: block; margin-left: auto; margin-right: auto;">
                    <line x1="50" y1="200" x2="380" y2="200" style="stroke:black;stroke-width:1" />
                    <line x1="50" y1="50" x2="50" y2="200" style="stroke:black;stroke-width:1" />
                    <text x="40" y="45" style="font-size:10px; text-anchor:end;">흑자</text>
                    <text x="40" y="128" style="font-size:10px; text-anchor:end;">0</text>
                    <text x="40" y="205" style="font-size:10px; text-anchor:end;">적자</text>
                    <text x="50" y="215" style="font-size:10px; text-anchor:middle;">T₀</text>
                    <text x="130" y="215" style="font-size:10px; text-anchor:middle;">T₁</text>
                    <text x="230" y="215" style="font-size:10px; text-anchor:middle;">T₂</text>
                    <text x="330" y="215" style="font-size:10px; text-anchor:middle;">T₃</text>
                    <text x="370" y="215" style="font-size:10px; text-anchor:middle;">시간</text>
                    <text x="15" y="128" style="font-size:10px; writing-mode:tb; text-anchor:middle;">무역수지</text>
                    <line x1="50" y1="125" x2="380" y2="125" style="stroke:gray;stroke-width:0.5;stroke-dasharray:4;" />
                    <path d="M 50 125 Q 90 180, 130 190 T 230 125 Q 280 90, 330 80 L 370 75" style="stroke:blue;stroke-width:2;fill:none;" />
                    <circle cx="50" cy="125" r="2" style="fill:blue;" />
                    <circle cx="130" cy="190" r="2" style="fill:blue;" />
                    <circle cx="230" cy="125" r="2" style="fill:blue;" />
                    <circle cx="330" cy="80" r="2" style="fill:blue;" />
                    <text x="130" y="100" style="font-size:10px; text-anchor:middle;">A 구간 (T₀-T₁)</text>
                    <text x="200" y="150" style="font-size:10px; text-anchor:middle;">B 구간 (T₁-T₂)</text>
                    <text x="300" y="60" style="font-size:10px; text-anchor:middle;">C 구간 (T₂-T₃ 이후)</text>
                </svg>
            </td>
        </tr>
    </table>
    <div style="margin-left: 1em; margin-top: 7px;">
    <div style="text-indent: -1.5em; padding-left: 1.5em;">① A 구간(T<sub>0</sub>~T<sub>1</sub>)에서는 환율 상승에도 불구하고 수출입 물량의 단기적 경직성으로 인해 가격 효과가 두드러져, 자국 화폐 기준 수입액이 증가하면서 무역수지가 악화된다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">② A 구간(T<sub>0</sub>~T<sub>1</sub>)이 형성되는 것은 기존 수출입 계약 물량이 일정 기간 유지되고, 생산 및 소비 패턴 변경에 시간이 소요되어 물량 조정이 지연되기 때문이다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">③ B 구간(T<sub>1</sub>~T<sub>2</sub>)에서는 가격 변동에 따른 물량 효과가 점차 나타나기 시작하여 수출 물량이 늘고 수입 물량이 줄면서 무역수지가 개선되기 시작한다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">④ 만약 T<sub>0</sub> 시점에서 수출입 상품의 가격 탄력성이 현재 그래프가 가정하는 것보다 더 크다면, T<sub>1</sub> 시점의 무역수지 적자 폭은 더 깊어지고 T<sub>2</sub> 시점은 더 늦춰질 것이다.</div>
    <div style="text-indent: -1.5em; padding-left: 1.5em;">⑤ C 구간(T<sub>2</sub>~T<sub>3</sub> 이후)에서는 물량 효과가 가격 효과를 압도하여 무역수지가 지속적으로 개선되거나 흑자 상태를 유지하며, 이는 수출입 가격 탄력성이 클수록 더 뚜렷하게 나타난다.</div>
    </div>
    </div>
    <br>
    """, unsafe_allow_html=True)

st.write("""


---

### 5️⃣ 전용 Fine-tuned AI 모델

##### 일반적인 AI 모델과 달리 수능 국어 지문 작성에 특화된 모델을 사용합니다.

- KSAT Agent는 1000개 이상의 데이터를 학습한 전용 AI 모델을 사용합니다.
- 수능 독서 지문 특유의 문체, 전개 방식을 내재화하여 인상적인 지문 작성 능력을 갖추고 있습니다.

##### AI 모델 학습 과정

- 적은 수의 기출 지문만으로도 과적합 없이 효과적인 학습이 가능하도록, 적절한 데이터 증강 기법을 적용하였습니다.
- 수십 번의 실험 끝에 최적의 하이퍼파라미터를 찾아 가장 효과적인 학습을 이끌어냈습니다.



""", unsafe_allow_html=True)

st.image(file_path4, output_format="auto", width=700)

st.write("""

---

### 6️⃣ AI Agent 시스템

- 최신 LangGraph 프레임워크를 활용하여 AI 에이전트 시스템을 구축하였습니다.
- 사용자와 여러 AI 에이전트 간의 상호작용 및 협업 과정을 최적화하였습니다.
- GPT 4.1, Claude 4.0, Gemini 2.5 Pro 등 작업 특성에 맞는 다양한 AI 모델들을 활용했습니다.
- 기출 DB를 탑재하여, AI 에이전트가 기출 문제를 자유롭게 참고할 수 있도록 하였습니다.

##### 에이전트 구조도
""")

stmd.st_mermaid(f"""
flowchart TD
    %% Supervisor 중심 워크플로우 (단방향 흐름)
    
    S["Supervisor"]:::super
    
    H(["Human Input"]):::user
    W["Passage Editor"]:::edit
    V["Question Editor"]:::valid
    F(["Finish"]):::result
    
    H --> S
    S --> W
    W --> V
    V --> F
    
    %% Supervisor 연결
    S <-.-> W
    S <-.-> V
    S <-.-> F
    
    %% 스타일링
    classDef user fill:#cce5ff,stroke:#0066cc,stroke-width:1px
    classDef super fill:#ffe6cc,stroke:#ff9933,stroke-width:2px,color:#ff6600,font-weight:bold
    classDef edit fill:#f9ddff,stroke:#cc66ff,stroke-width:1px
    classDef valid fill:#e6e6ff,stroke:#6666ff,stroke-width:1px
    classDef result fill:#f2f2f2,stroke:#666666,stroke-width:1px
""", zoom=False, show_controls=False)