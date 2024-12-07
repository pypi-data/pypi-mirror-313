import pytest
import pandas as pd
from unittest.mock import Mock, patch
from tangbao.retrievers import BM25Retriever, HybridRetrieverApollo, extract_docs_from_apollo_vs, rrf

# Test data fixtures
@pytest.fixture
def sample_corpus():
    return [
        {"text": "This is document one", "metadata": {"id": 1}},
        {"text": "This is document two", "metadata": {"id": 2}},
        {"text": "Another document three", "metadata": {"id": 3}}
    ]

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Content': ['Document one', 'Document two'],
        'Metadata': [{'id': 1}, {'id': 2}]
    })

@pytest.fixture
def mock_apollo():
    with patch('tangbao.retrievers.Apollo') as mock:
        yield mock

class TestBM25Retriever:
    def test_init(self, sample_corpus):
        retriever = BM25Retriever(sample_corpus)
        assert retriever.corpus == sample_corpus
        assert retriever.corpus_tokens is None

    def test_index_corpus(self, sample_corpus):
        retriever = BM25Retriever(sample_corpus)
        retriever.index_corpus()
        assert retriever.corpus_tokens is not None

    def test_query_corpus(self, sample_corpus):
        retriever = BM25Retriever(sample_corpus)
        retriever.index_corpus()
        results = retriever.query_corpus("document one", k=2)
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert all(key in results[0] for key in ['metadata', 'text', 'score'])

    def test_query_corpus_no_matches(self, sample_corpus):
        retriever = BM25Retriever(sample_corpus)
        retriever.index_corpus()
        results = retriever.query_corpus("xyzabc123", k=2)
        assert len(results) == 0

class TestHybridRetrieverApollo:
    def test_init(self, sample_df, mock_apollo):
        retriever = HybridRetrieverApollo(
            df=sample_df,
            index_name="test_index",
            embedding_model="test_model"
        )
        assert isinstance(retriever.bm25_retriever, BM25Retriever)
        assert retriever.index_name == "test_index"
        assert retriever.embedding_model == "test_model"

    def test_query_indices(self, sample_df, mock_apollo):
        # Mock Apollo response
        mock_apollo_response = {
            "docs": [
                {
                    "text": "Document one",
                    "metadata": {"id": 1},
                    "score": 0.9
                }
            ]
        }
        
        mock_apollo.return_value.query_index.return_value = mock_apollo_response
        
        retriever = HybridRetrieverApollo(
            df=sample_df,
            index_name="test_index",
            embedding_model="test_model"
        )
        
        results = retriever.query_indices(
            user_query="test query",
            num_chunks=2,
            keyword_weight=0.5
        )
        
        assert isinstance(results, list)
        assert all(key in results[0] for key in ['rank', 'text', 'metadata'])

    def test_query_indices_with_no_weight(self, sample_df, mock_apollo):
        # Similar to above but without keyword_weight
        pass

def test_extract_docs_from_apollo_vs():
    response = {
        "docs": [
            {
                "text": "doc1",
                "metadata": {"id": 1},
                "score": 0.9
            },
            {
                "text": "doc2",
                "metadata": {"id": 2},
                "score": 0.8
            }
        ]
    }
    
    result = extract_docs_from_apollo_vs(response)
    assert len(result) == 2
    assert all(key in result[0] for key in ['text', 'metadata', 'score'])
    assert result[0]['text'] == "doc1"
    assert result[0]['score'] == 0.9

def test_rrf():
    rank_lists = [
        [
            {"text": "doc1", "metadata": {"id": 1}, "score": 0.9},
            {"text": "doc2", "metadata": {"id": 2}, "score": 0.8}
        ],
        [
            {"text": "doc2", "metadata": {"id": 2}, "score": 0.95},
            {"text": "doc1", "metadata": {"id": 1}, "score": 0.85}
        ]
    ]
    
    # Test with default weights
    result = rrf(rank_lists)
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(key in result[0] for key in ['rank', 'text', 'metadata'])
    
    # Test with custom weights
    result_weighted = rrf(rank_lists, weights=[0.7, 0.3])
    assert isinstance(result_weighted, list)
    assert len(result_weighted) > 0

def test_rrf_empty_lists():
    result = rrf([])
    assert len(result) == 0

def test_rrf_single_list():
    rank_list = [
        {"text": "doc1", "metadata": {"id": 1}, "score": 0.9}
    ]
    result = rrf([rank_list])
    assert len(result) == 1
    assert result[0]['text'] == "doc1" 