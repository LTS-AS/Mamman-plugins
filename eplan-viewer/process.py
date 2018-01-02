import pandas

if __name__ == '__main__':
    df = pandas.read_json('data.json', orient='records')
    #df = df.sort_values('')
    df = df.groupby(['file_path_relative']).count()
    df = df.add_suffix('_count').reset_index()
    #df = df.sort_values('file_walkpath_relative_count', ascending = False)
    print(df)