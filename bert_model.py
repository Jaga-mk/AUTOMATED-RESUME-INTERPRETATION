from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("🔄 Loading BERT model... (this may take time first run)")

try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ BERT model loaded successfully")
except Exception as e:
    print("❌ Error loading BERT model:", e)


def bert_similarity(resumes, job_desc):
    try:
        print("🔄 Encoding resumes and job description...")

        all_texts = resumes + [job_desc]

        embeddings = model.encode(all_texts)

        print("✅ Encoding completed")

        job_vector = embeddings[-1]
        resume_vectors = embeddings[:-1]

        scores = cosine_similarity([job_vector], resume_vectors)[0]

        print("✅ Similarity calculated")

        return scores

    except Exception as e:
        print("❌ Error in similarity calculation:", e)
        return []