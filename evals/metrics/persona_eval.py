"""
Persona & Empathy Alignment Evaluator (LLM-as-a-Judge)
Scores Nexus AI's generated response against core personality traits (0.0 to 1.0).
"""

import json

def evaluate_persona_alignment(response_text: str, target_traits: list) -> dict:
    """
    Evaluates whether the generated response exhibits warm, curious, and empathetic persona traits.
    """
    scores = {}
    
    # Heuristic checks
    is_corporate = any(phrase in response_text.lower() for phrase in ["as an ai", "how can i help you today", "i am an assistant"])
    is_warm = len(response_text) > 20 and not is_corporate

    for trait in target_traits:
        if trait in ["WARMTH", "EMPATHY"]:
            scores[trait] = 0.9 if is_warm else 0.4
        elif trait == "CURIOSITY":
            scores[trait] = 0.85 if "?" in response_text else 0.5
        else:
            scores[trait] = 0.8

    avg_score = sum(scores.values()) / len(scores) if scores else 0.0
    return {
        "overall_score": round(avg_score, 2),
        "trait_scores": scores,
        "is_corporate_flag": is_corporate
    }

if __name__ == "__main__":
    sample_response = "I hear you — balancing tight deadlines when anxiety kicks in is incredibly exhausting. What part of the project is weighing on you most right now?"
    result = evaluate_persona_alignment(sample_response, ["WARMTH", "EMPATHY", "CURIOSITY"])
    print("Persona Eval Result:", json.dumps(result, indent=2))
