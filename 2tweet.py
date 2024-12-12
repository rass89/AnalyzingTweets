# Import necessary libraries
import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the stopwords file
with open('stopwords_en.txt', 'r') as f:
    stopwords = set(f.read().splitlines())

# Load the tweets CSV file
tweets_df = pd.read_csv('tweets.csv', names=['Sender', 'Timestamp', 'Text'], encoding='latin-1')

# Function to Lowercase and remove stopwords
def clean_text(text):
    words = [word.lower() for word in text.split() if word.lower() not in stopwords]
    return ' '.join(words)

# Apply the clean_text function to the Text column
tweets_df['Cleaned_Text'] = tweets_df['Text'].apply(clean_text)

# 1. Print the 10 most active senders
most_active_senders = tweets_df['Sender'].value_counts().head(10)
print("Most active senders:\n", most_active_senders)

# 2. Print the 10 most retweeted tweets (tweets starting with RT)
retweets = tweets_df[tweets_df['Text'].str.startswith('RT')]
most_retweeted = retweets['Text'].value_counts().head(10)
print("\nMost retweeted tweets:\n", most_retweeted)

# 3. Print the 10 most cited screen names
def extract_mentions(text):
    return re.findall(r'@\w+', text)

tweets_df['Mentions'] = tweets_df['Text'].apply(extract_mentions)
all_mentions = [mention for mentions in tweets_df['Mentions'] for mention in mentions]
most_cited = Counter(all_mentions).most_common(10)
print("\nMost cited screen-names:\n", most_cited)

# Check if cited screen names are among the most active senders
for mention, count in most_cited:
    is_active = mention in most_active_senders.index
    print(f"{mention}: {'Yes' if is_active else 'No'}")

# 4. Print the 10 most popular hashtags
def extract_hashtags(text):
    return re.findall(r'#\w+', text)

tweets_df['Hashtags'] = tweets_df['Text'].apply(extract_hashtags)
all_hashtags = [hashtag for hashtags in tweets_df['Hashtags'] for hashtag in hashtags]
most_popular_hashtags = Counter(all_hashtags).most_common(10)
print("\nMost popular hashtags:\n", most_popular_hashtags)

# 5. Sort by timestamp then split into 5 subsets
tweets_df = tweets_df.sort_values(by='Timestamp')
num_tweets = len(tweets_df)
subset_size = num_tweets // 5

for i in range(5):
    subset = tweets_df.iloc[i*subset_size:(i+1)*subset_size]
    start_time = subset['Timestamp'].min()
    end_time = subset['Timestamp'].max()
    text = ' '.join(subset['Cleaned_Text'])

    # Generate and display the wordcloud
    wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)

    # Show the word cloud
    plt.figure(figsize=(8,6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"WordCloud for Subset {i+1} (Time: {start_time} - {end_time})")
    plt.show()

