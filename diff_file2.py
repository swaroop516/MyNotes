from sklearn.metrics.pairwise import cosine_similarity
user_game['cos similarity']= 0.0
for user in user_game.index:
    cos=cosine_similarity(user_game.loc[5250].values.reshape(1,-1), user_game.loc[user].values.reshape(1, -1))
    user_game['cos similarity'][user]=cos
sim_user = user_game[user_game['cos similarity'].astype(int) != 1]['cos similarity'].sort_values(ascending=False).head(15).index.to_list()
sim_games = cleaned_df[cleaned_df['user_id'].isin(sim_user)]['game'].unique().tolist()
user_games = cleaned_df[(cleaned_df['user_id']==5250) & (cleaned_df['game'].isin(sim_games))]['game'].unique().tolist()
recom_games = list(set(sim_games) - set(user_games))