def explain_prediction(model, vectorizer, text, top_n=8):
    try:
        names = vectorizer.get_feature_names_out()
        coefs = model.coef_[0]

        vec = vectorizer.transform([text])
        indices = vec.nonzero()[1]

        scores = [(names[i], coefs[i]) for i in indices]

        fake_words = sorted(scores, key=lambda x: x[1])[:top_n]
        real_words = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]

        return fake_words, real_words
    except:
        return [], []