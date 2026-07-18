import streamlit as st

from preprocess import clean_text
from predict import predict_sentiment
from response_generator import generate_response
from entity_extractor import extract_entities

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="AI Customer Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================================
# PRODUTOS
# ==========================================================

products = [
    {
        "id": 1,
        "name": "Notebook Dell Inspiron",
        "image": "images/notebook.jpg",
        "price": "R$ 4.599",
        "rating": 4.8
    },
    {
        "id": 2,
        "name": "iPhone 15",
        "image": "images/iphone.jpg",
        "price": "R$ 5.299",
        "rating": 4.9
    },
    {
        "id": 3,
        "name": "Samsung Galaxy S24",
        "image": "images/galaxy.jpg",
        "price": "R$ 4.299",
        "rating": 4.8
    },
    {
        "id": 4,
        "name": "Smart TV LG 55",
        "image": "images/tv.jpg",
        "price": "R$ 2.899",
        "rating": 4.7
    },
    {
        "id": 5,
        "name": "JBL Tune 770",
        "image": "images/jbl.jpg",
        "price": "R$ 399",
        "rating": 4.6
    }
]

# ==========================================================
# SESSION STATE
# ==========================================================

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("🤖 AI Customer Assistant")
st.write("Escolha um produto para avaliar.")

# ==========================================================
# SELEÇÃO DO PRODUTO
# ==========================================================

st.subheader("Selecione o produto")

nomes = [p["name"] for p in products]

produto_escolhido = st.selectbox(
    "Produto",
    nomes
)

for p in products:
    if p["name"] == produto_escolhido:
        st.session_state.selected_product = p
        break

# ==========================================================
# EXIBIÇÃO DO PRODUTO
# ==========================================================

produto = st.session_state.selected_product

st.divider()

col1, col2 = st.columns([1,2])

with col1:
    st.image(produto["image"], use_container_width=True)

with col2:
    st.subheader(produto["name"])
    st.write(f"💰 **Preço:** {produto['price']}")
    st.write(f"⭐ **Avaliação:** {produto['rating']}")


st.divider()

# ==================================================
# AVALIAÇÃO
# ==================================================

st.subheader("📝 Avaliação do Cliente")

review = st.text_area(
    "",
    height=220,
    placeholder="""
Exemplo:

Olá, meu nome é Rafael.

Gostei muito do produto, a qualidade é excelente.

Porém a entrega demorou alguns dias.
"""
)

# ==================================================
# ANÁLISE
# ==================================================

if st.button(
    "🚀 Analisar Avaliação",
    use_container_width=True
):

    if not review.strip():

        st.warning(
            "Digite uma avaliação."
        )
        st.stop()

    cleaned_text = clean_text(
        review
    )

    result = predict_sentiment(
        cleaned_text
    )

    entities = extract_entities(
        review
    )

    response = generate_response(
        result["label"],
        produto["name"]
    )

    st.divider()

    # ==========================================
    # RESULTADO
    # ==========================================

    left, right = st.columns(2)

    with left:

        st.subheader("📊 Resultado")

        if result["label"] == "POSITIVE":

            st.success(
                "😊 Cliente Satisfeito"
            )

        else:

            st.error(
                "😕 Cliente Insatisfeito"
            )

        st.metric(
            "Confiança",
            f"{result['score']:.2%}"
        )

        st.metric(
            "Produto",
            produto["name"]
        )

    with right:

        st.subheader(
            "🧠 Informações Detectadas"
        )

        st.json({
            "Cliente":
            entities.get(
                "customer_name"
            ),

            "Produto":
            entities.get(
                "product"
            )if entities.get("product") else produto["name"],

            "Gostou do Produto":
            entities.get(
                "liked_product"
            ),

            "Problema na Entrega":
            entities.get(
                "delivery_issue"
            )
        })

    # ==========================================
    # RESPOSTA
    # ==========================================

    st.divider()

    st.subheader(
        "💬 Resposta Sugerida"
    )

    st.markdown(
        f"""
        <div class="response-box">
            {response}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("📋 Resumo")

    st.write(
    f"✅ Produto analisado: **{produto['name']}**"
    )

    if entities.get("customer_name"):
        st.write(
            f"✅ Cliente identificado: **{entities['customer_name']}**"
        )

    if entities.get("liked_product"):
        st.write(
            "✅ Cliente demonstrou satisfação com o produto."
        )

    if entities.get("delivery_issue"):
        st.write(
            "✅ Possível problema relacionado à entrega."
        )
