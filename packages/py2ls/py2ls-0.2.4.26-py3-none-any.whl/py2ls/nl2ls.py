from . import translator,ips,plot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


def detect(text, method: str = "vader", nb_model=None, device=-1,overall_method="major",overall_threhold=0.8,overall_weight=None,plot_=True,verbose=True, **kwargs) -> dict:
    """
    Analyze the sentiment of a text or a list of texts using different methods.

    Parameters:
    - text (str or list of str): The text(s) to analyze. Can be a single text or a list of texts.
    - method (str): The method to use ('vader', 'textblob', 'naive_bayes', 'transformers', 'senta').
    - nb_model (Optional[MultinomialNB]): Pre-trained Naive Bayes model (required if method='naive_bayes').
    - vectorizer (Optional[TfidfVectorizer]): Vectorizer trained with Naive Bayes model (required if method='naive_bayes').
    - device (int): Device to run the model on (-1 for CPU, 0 for GPU).
    - transformer_model_name (str): Transformer model name for 'transformers' method.

    Returns:
    - dict: A dictionary with sentiment score, sentiment label, analysis method, and language.
    """
    result = {
        "method": method,
        "score": None,
        "label": None,
        "language": None,
    }

    methods=['vader','textblob','naive_bayes','transformer(not ready)','senta(not ready)']
    if ips.run_once_within(10, reverse=True) and verbose:
        print(f"methods: {methods}")
        
    overall_methods=["majority","average","mean","threshold","weighted","detailed"]
    if ips.run_once_within(10, reverse=True) and verbose:
        print(f"overall_methods: {overall_methods}")
    # If the input is a list of texts, loop through each one
    if isinstance(text, list):
        results = []
        for text_ in text:
            results.append(detect_single_text(text_, method=method, nb_model=nb_model, device=device, **kwargs))
        res_overall=get_overall_results(results, method=overall_method, threshold=overall_threhold, weight=overall_weight)
        if plot_:
            res_detail=get_overall_results(results, method='detail', threshold=overall_threhold, weight=overall_weight)
            plot.pie(res_detail["label"].value_counts(),explode=None,verbose=False)
        return res_overall
    else:
        return detect_single_text(text=text, method=method, nb_model=nb_model, device=device, **kwargs)


def detect_single_text(text: str, method: str = "vader", nb_model=None, device=-1, **kwargs) -> dict:
    """
    Analyze the sentiment of a text using different methods.

    Parameters:
    - text (str): The text to analyze.
    - method (str): The method to use ('vader', 'textblob', 'naive_bayes', 'transformers').
    - nb_model (Optional[MultinomialNB]): Pre-trained Naive Bayes model (required if method='naive_bayes').
    - vectorizer (Optional[TfidfVectorizer]): Vectorizer trained with Naive Bayes model (required if method='naive_bayes').
    - transformer_model_name (str): Transformer model name for 'transformers' method.

    Returns:
    - dict: A dictionary with sentiment score, sentiment label, analysis method, and language.
    """
    result = {
        "text":text,
        "method": method,
        "score": None,
        "label": None,
        "language": None,
    }

    # Detect language for additional insights
    language = translator.detect_lang(text)
    result["language"] = language
    if language != "English" and method in ["vader", "textblob", "naive_bayes"]:
        print("Detected non-English language, results may be inaccurate.")
    methods=['vader','textblob','naive_bayes','transformer(not ready)','senta(not ready)'] 
    method=ips.strcmp(method,methods)[0]
    if method == "vader":
        import nltk, os
        from nltk.sentiment import SentimentIntensityAnalyzer

        # check if it is downloaded
        is_local = os.path.isfile(
            os.path.join(nltk.data.path[0], "sentiment", "vader_lexicon.zip")
        )
        if not is_local:
            nltk.download("vader_lexicon")
        try:
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(text)
            result["score"] = scores["compound"]
            result["label"] = (
                "Positive"
                if scores["compound"] >= 0.05
                else "Negative" if scores["compound"] <= -0.05 else "Neutral"
            )
        except Exception as e:
            print(f"Error in VADER analysis: {e}")

    elif method == "textblob":
        from textblob import TextBlob

        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            result["score"] = polarity
            result["label"] = (
                "Positive"
                if polarity > 0
                else "Negative" if polarity < 0 else "Neutral"
            )
        except Exception as e:
            print(f"Error in TextBlob analysis: {e}")

    elif method == "naive_bayes":
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.feature_extraction.text import TfidfVectorizer

        try:
            if nb_model is None or vectorizer is None:
                from sklearn.model_selection import train_test_split

                # Sample data for Naive Bayes training if model not provided
                sample_texts = [
                    "I love this product",
                    "I hate this product",
                    "It's okay, not great",
                    "Absolutely fantastic!",
                    "Not satisfied",
                ]
                sample_labels = [1, 0, 0, 1, 0]  # 1 = Positive, 0 = Negative

                # Train Naive Bayes model
                vectorizer = TfidfVectorizer()
                X_train_tfidf = vectorizer.fit_transform(sample_texts)
                nb_model = MultinomialNB()
                nb_model.fit(X_train_tfidf, sample_labels)

            transformed_text = vectorizer.transform([text])
            prediction = nb_model.predict(transformed_text)[0]
            result["score"] = max(nb_model.predict_proba(transformed_text)[0])
            result["label"] = "Positive" if prediction == 1 else "Negative"

        except Exception as e:
            print(f"Error in Naive Bayes analysis: {e}")
    elif method=="transformer":
        try:
            from transformers import pipeline
            # Load pre-trained sentiment analysis pipeline with a Chinese model
            classifier = pipeline('sentiment-analysis', model='bert-base-chinese', device=device)
            analysis_result = classifier(text)
            result["score"] = analysis_result[0]['score']
            result["label"] = analysis_result[0]['label']
        except Exception as e:
            print(f"Error in Transformer analysis: {e}")
    elif method == "senta":
        from transformers import pipeline

        try:
            # Load the Senta model for sentiment analysis
            classifier = pipeline('sentiment-analysis', model='junnyu/senta', device=device)
            analysis_result = classifier(text)
            
            # Senta model output will be a list with one result (since it's single text input)
            result["score"] = analysis_result[0]["score"]
            result["label"] = analysis_result[0]["label"]
            
        except Exception as e:
            print(f"Error in Senta analysis: {e}")

    else:
        print(
            f"Unknown method '{method}'. Available methods: 'vader', 'textblob', 'naive_bayes', 'transformers'"
        )
        raise ValueError(
            f"Unknown method '{method}'. Available methods: 'vader', 'textblob', 'naive_bayes', 'transformers'"
        )

    return result

def get_overall_results(results, method="majority", threshold=0.8, weight=None,verbose=False):
    from collections import Counter
    """
    Aggregates sentiment analysis results based on the selected method.

    Parameters:
    - results (list): A list of sentiment analysis results, each being a dictionary.
    - method (str): The aggregation method to use ('majority', 'average', 'threshold', 'weighted', 'detailed').
    - threshold (float): Confidence threshold for 'threshold' method.
    - weight (dict): Optional dictionary for weighted aggregation (e.g., model name as key and weight as value).

    Returns:
    - dict: Aggregated sentiment result with final label and score.
    """
    def majority_voting(results):
        """Aggregates sentiment using majority voting."""
        labels = [result['label'] for result in results]
        label_counts = Counter(labels)
        final_label = label_counts.most_common(1)[0][0]  # Get the most common label
        return {"label": final_label}


    def average_score(results):
        """Aggregates sentiment by calculating the average score."""
        scores = [result['score'] for result in results]
        avg_score = sum(scores) / len(scores)
        
        if avg_score > 0.05:
            label = 'Positive'
        elif avg_score < -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'
            
        return {"score": avg_score, "label": label}


    def confidence_threshold(results, threshold=0.8):
        """Aggregates sentiment based on a confidence threshold."""
        labels = [result['label'] for result in results]
        label_counts = Counter(labels)
        total_results = len(results)
        
        for label, count in label_counts.items():
            if count / total_results >= threshold:
                return {"label": label}
        
        return {"label": 'Neutral'}  # If no label exceeds the threshold, return neutral


    def weighted_average(results, weight=None):
        """Aggregates sentiment based on a weighted average."""
        if weight is None:
            weight = {"vader": 2} 

        weighted_scores = 0
        total_weight = 0
        
        for result in results:
            model = result.get('method', 'default')
            model_weight = weight.get(model, 1)  # Default weight is 1 if model not in weight dict
            weighted_scores += result['score'] * model_weight
            total_weight += model_weight
        
        avg_weighted_score = weighted_scores / total_weight
        
        # Assign label based on weighted average score
        if avg_weighted_score > 0.05:
            label = 'Positive'
        elif avg_weighted_score < -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'
        
        return {"score": avg_weighted_score, "label": label}

    def detailed_output(results,verbose=False):
        """Prints the detailed sentiment results."""
        for result in results:
            if verbose:
                print(f"Label: {result['label']} | Score: {result['score']}")
        return {"detailed_results": results}
    overall_methods=["majority","average","mean","threshold","weighted","detailed"] 
    method=ips.strcmp(method, overall_methods)[0]
    if method == "majority":
        return majority_voting(results)

    elif method in ["mean","average"]:
        return average_score(results)

    elif method == "threshold":
        return confidence_threshold(results, threshold)

    elif method == "weighted":
        return weighted_average(results, weight)

    elif method == "detailed":
        return pd.DataFrame(results)
    else:
        raise ValueError(f"Unknown method '{method}'. Available methods: 'majority', 'average', 'threshold', 'weighted', 'detailed'")


