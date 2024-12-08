from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

def word_cloud(text_data):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off') 
    plt.show()

def tokenize_text(text):
    """
    Tokenizes the input text into words using regular expressions.
    Returns a list of alphanumeric words.
    """
    return re.findall(r'\b\w+\b', text.lower())

# when include_others=False 100% is only these n words
def word_frequency_pie_chart(text, include_others=True, n=10):
    """
    Creates a pie chart of word frequency distribution from the input text.
    """
    # Tokenize the text
    words = tokenize_text(text)
    
    # Count word occurrences
    word_counts = Counter(words)
    
    # Get the n most common words
    most_common = word_counts.most_common(n)
    total_words = sum(word_counts.values())
    
    if include_others:
        # Compute "Others" category
        other_count = total_words - sum(count for _, count in most_common)
        most_common.append(("Others", other_count))
    
    # Extract labels and sizes for the pie chart
    labels = [word for word, _ in most_common]
    sizes = [count / total_words * 100 for _, count in most_common]
    
    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Word Frequency Distribution (Pie Chart)')
    plt.show()

# when include_others=False 100% is still all words (including others, but they are not displayed)
def word_frequency_bar_chart(text, include_others=True, n=10):
    """
    Creates a bar chart of word frequency distribution from the input text.
    """
    # Tokenize the text
    words = tokenize_text(text)
    
    # Count word occurrences
    word_counts = Counter(words)
    
    # Get the n most common words
    most_common = word_counts.most_common(n)
    total_words = sum(word_counts.values())
    
    if include_others:
        # Compute "Others" category
        other_count = total_words - sum(count for _, count in most_common)
        most_common.append(("Others", other_count))
    
    # Extract labels and sizes for the bar chart
    labels = [word for word, _ in most_common]
    sizes = [count / total_words * 100 for _, count in most_common]
    
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(labels, sizes)
    plt.xlabel('Words')
    plt.ylabel('Percentage of Occurrences')
    plt.title('Word Frequency Distribution (Bar Chart)')
    plt.xticks(rotation=45)
    plt.show()