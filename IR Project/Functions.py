import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import os
import string
import PyPDF2
import numpy as np
from pyparsing import originalTextFor
nltk.download('stopwords')

def read_pdf_content(folder_path):

  text_content = []
  for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
      file_path = os.path.join(folder_path, filename)
      with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        page_text = ""
        for page_num in range(num_pages):
          page = pdf_reader.pages[page_num]
          page_text += page.extract_text()

        text_content.append(page_text.strip())  # Remove leading/trailing whitespace
  return text_content

def preprocess_text(text):
 
  # Tokenization (split text into words)
  no_punct_text = "".join([char for char in text if char not in string.punctuation])
  tokens = no_punct_text.lower().split()

  # Remove stop words (optional)
  stop_words = set(stopwords.words('english'))
  tokens = [token for token in tokens if token not in stop_words]

  # Stemming or Lemmatization (optional)
  # Choose between stemming (reduce words to their root form) or lemmatization (convert words to their dictionary form)
  stemmer = PorterStemmer()  # For stemming
  # lemmatizer = WordNetLemmatizer()  # For lemmatization (uncomment to use)

  # Apply stemming or lemmatization
  preprocessed_tokens = []
  for token in tokens:
    # Use either stemming or lemmatization based on your choice
    # preprocessed_tokens.append(lemmatizer.lemmatize(token))
    preprocessed_tokens.append(stemmer.stem(token))

  return ' '.join(preprocessed_tokens)  # Join preprocessed tokens back into text

def preprocess_folder(text_content):

  preprocessed_data = []
  for text in text_content:
        preprocessed_content = preprocess_text(text)
        preprocessed_data.append(preprocessed_content)
        
  return preprocessed_data

folder_path = "Dataset"
readed=read_pdf_content(folder_path)

preprocessed_hotel_data = preprocess_folder(readed) #preprocess hotel data

def create_inverted_index(preprocessed_data):

  inverted_index = {}
  for doc_id, doc_content in enumerate(preprocessed_data):
    for term in doc_content.split():
      if term not in inverted_index:
        inverted_index[term] = []
      inverted_index[term].append(doc_id)
  return inverted_index

inverted_index = create_inverted_index(preprocessed_hotel_data) #inverted index for preprocessed hotel data

unique_terms = set()  # Collect unique terms across all documents

def create_incidence_matrix(preprocessed_data):
 
  unique_terms = set()  # Collect unique terms across all documents

  # Find all unique terms
  for doc_content in preprocessed_data:
    unique_terms.update(doc_content.split())

  # Create the matrix with rows (documents) and columns (terms)
  num_documents = len(preprocessed_data)
  num_terms = len(unique_terms)
  incidence_matrix = [[0 for _ in range(num_terms)] for _ in range(num_documents)]

  # Populate the matrix (1 for term existence, 0 otherwise)
  term_to_index = {term: i for i, term in enumerate(unique_terms)}  # Map term to its column index
  for doc_id, doc_content in enumerate(preprocessed_data):
    for term in doc_content.split():
      term_index = term_to_index[term]
      incidence_matrix[doc_id][term_index] = 1

  return incidence_matrix

incidence_matrix = create_incidence_matrix(preprocessed_hotel_data)  #incidence matrix for preprocessed hotel data

def create_biword_index(preprocessed_data):

  biword_index = {}
  for doc_id, doc_content in enumerate(preprocessed_data):
    tokens = doc_content.split()
    for i in range(len(tokens) - 1):  # Iterate up to second-to-last word to create bigrams
      bigram = f"{tokens[i]} {tokens[i+1]}"
      if bigram not in biword_index:
        biword_index[bigram] = []
      biword_index[bigram].append(doc_id)
  return biword_index

biword_index = create_biword_index(preprocessed_hotel_data)   #bi word index for preprocessed hotel data

def create_positional_index(preprocessed_data):

  positional_index = {}
  for doc_id, doc_content in enumerate(preprocessed_data):
    tokens = doc_content.split()
    for i, term in enumerate(tokens):
      if term not in positional_index:
        positional_index[term] = {}
      if doc_id not in positional_index[term]:
        positional_index[term][doc_id] = []
      positional_index[term][doc_id].append(i)  # Store term positions within the document
  return positional_index

positional_index = create_positional_index(preprocessed_hotel_data)  #positional index for preprocessed hotel data

def search_inverted_index(inverted_index, search_query, operator=""):

  # Split the search query into terms (already preprocessed)
  search_terms = search_query.split()

  # Handle default search (all terms as keywords) if no operator is specified
  if operator.upper() not in ("AND", "OR"):
    operator = " "  # Use space as default separator (implicit AND)
    search_query = " ".join(search_terms)  # Combine terms for keyword search

  # Perform search based on operator
  if operator == "AND":
    matching_hotel_ids = set(inverted_index[search_terms[0]])  # Start with all docs containing the first term
    for term in search_terms[1:]:
      matching_hotel_ids = matching_hotel_ids.intersection(set(inverted_index.get(term, [])))  # AND: documents with all terms
  elif operator == "OR":
    matching_hotel_ids = set()
    for term in search_terms:
      matching_hotel_ids.update(set(inverted_index.get(term, [])))  # OR: documents with any term
  else:
    # Keyword search (implicit AND): documents containing all terms (space separated)
    matching_hotel_ids = set()
    for doc_id, doc_content in enumerate(inverted_index.keys()):  # Iterate through all documents (keys in inverted index)
      if all(term in doc_content for term in search_terms):  # Check if all search terms exist in the document content
        matching_hotel_ids.add(doc_id)

      # Retrieve original text using the mapping
  original_text_results = []
  for doc_id in matching_hotel_ids:
    original_text_results.append(originalTextFor[doc_id])  # Access original text using doc_id as index
  final = " \n /////////////////////// \n ".join(original_text_results)
  return final # Convert set to a list for consistency

# def search_incidence_matrix(incidence_matrix, search_query, operator="AND", hotel_data=None):
#   # Split the search query into terms (already preprocessed)
#   search_terms = search_query.split()

#   # Convert terms to column indices (assuming vocabulary order matches matrix columns)
#   term_indices = [set(unique_terms).index(term) for term in search_terms if term in set(unique_terms)]

#   # Perform search based on operator
#   if operator == "AND":
#     matching_hotel_ids = incidence_matrix[:, term_indices[0]].copy()  # Start with first term
#     for term_index in term_indices[1:]:
#       matching_hotel_ids = np.logical_and(matching_hotel_ids, incidence_matrix[:, term_index])  # AND: all elements must be 1
#   elif operator == "OR":
#     matching_hotel_ids = np.zeros(incidence_matrix.shape[0], dtype=bool)  # Initialize empty boolean array for OR
#     for term_index in term_indices:
#       matching_hotel_ids = np.logical_or(matching_hotel_ids, incidence_matrix[:, term_index])  # OR: at least one element must be 1
#   else:
#     raise ValueError(f"Invalid operator: {operator}")

#   # Get document IDs (row indices) of matching rows
#   matching_hotel_ids = list(np.where(matching_hotel_ids == True)[0])

#   # Return hotel data if available
# #   if hotel_data:
#   hotel_results = [hotel_data[id] for id in matching_hotel_ids]
#   final = " \n ///////////////////////////// \n ".join(hotel_results)
  
#   return final  # List comprehension to retrieve matching hotel content

def search_positional_index(positional_index, search_query,  hotel_data , proximity=None):

  # Split the search query into terms (already preprocessed)
  search_terms = search_query.split()

  # Perform term lookup and get documents for each term
  matching_hotel_ids = set(positional_index.get(term, {}).keys()) & set(positional_index.get(search_terms[0], {}).keys())  # Initial intersection for all terms
  for term in search_terms[1:]:
    matching_hotel_ids = matching_hotel_ids.intersection(set(positional_index.get(term, {}).keys()))  # Further intersection for subsequent terms
  # Proximity check (if specified)
  if proximity:
    filtered_hotel_ids = []
    for doc_id in matching_hotel_ids:
      term_positions = [positional_index[term][doc_id] for term in search_terms]  # Get positions of all search terms in the document
      # Check if any pair of terms appears within the proximity distance
      if any(abs(p1 - p2) <= proximity for term1, p1 in zip(search_terms, term_positions) for term2, p2 in zip(search_terms[1:], term_positions[1:])):
        filtered_hotel_ids.append(doc_id)
    matching_hotel_ids = set(filtered_hotel_ids)  # Update matching IDs based on proximity

  hotel_data_results = [hotel_data[doc_id] for doc_id in matching_hotel_ids] 
  final = " \n ///////////////////////////// \n ".join(hotel_data_results)
  
  return final  # Convert set to a list for consistency

def search_biword_index(biword_index, search_query , hotel_data):

  # Split the search query into two terms (assuming a bigram)
  search_terms = search_query.split()
  if len(search_terms) != 2:
    raise ValueError("Bi-word index search requires a phrase with two words.")

  # Create the bigram (consecutive word pair)
  bigram = " ".join(search_terms)

  # Lookup the bigram in the index
  matching_hotel_ids = biword_index.get(bigram, [])
  hotel_data_results = [hotel_data[doc_id] for doc_id in matching_hotel_ids] 
  final = " \n ///////////////////////////// \n ".join(hotel_data_results)
  return final


# Assuming you have the biword_index and search_query
# matching_hotel_ids = search_biword_index(biword_index, search_query)
# print(f"Hotels containing the phrase '{search_query}'