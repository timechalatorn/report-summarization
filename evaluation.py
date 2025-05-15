from rouge_score import rouge_scorer

def evaluate_summary(generated_summary, reference_summary):
    """
    Evaluates a generated summary using ROUGE against a reference summary.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_summary, generated_summary)

    print("\n📊 ROUGE Evaluation Results:")
    for k, v in scores.items():
        print(f"{k.upper()}:")
        print(f"  Precision: {v.precision:.4f}")
        print(f"  Recall:    {v.recall:.4f}")
        print(f"  F1 Score:  {v.fmeasure:.4f}")
