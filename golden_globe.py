import json
import pandas as pd

pd.options.display.max_colwidth = 200

# data = json.load(open('gg2018.json'))
df = pd.DataFrame(columns = ['text', 'id_str'])

df = pd.read_json('gg2018.json')
df['text'] = [str(u)for u in df['text']]
df['text'] = [u.encode('ascii', 'ignore') for u in df['text']]
df_count = df.groupby('text').count()
print(df_count.sort_values('id_strcount'))


# valid = 'nominee' in df['text']
df['text'] = [str(u)for u in df['text']]
df_useful = df.loc[df['text'].str.contains('Congratulation') & df['text'].str.contains('Best Performance by an Actor in a Motion Picture - Drama')].dropna()
# df_useful = df.loc[df['text'].str.contains('Congradulation') & df['text'].str.contains('Director') & df['text'].str.contains('Best')].dropna()
df_useful['text'] = [u.encode('ascii', 'ignore') for u in df_useful['text']]
print(df_useful['text'])
print(df_useful.groupby('text').count())

