from rag import rechercher_passages

question = "Quelles sont les règles concernant les retards ?"

passages = rechercher_passages(question)

for passage in passages:
    print(f"\nPage : {passage['page']}")
    print(f"Source : {passage['source']}")
    print(f"Distance : {passage['distance']:.4f}")
    print(f"Texte : {passage['texte'][:300]}...")