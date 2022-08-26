from sklearn.metrics.pairwise import cosine_similarity
user_game['cos similarity']= 0.0
for user in user_game.index:
  cos=cosine_similarity(user_game.loc[5250].values.reshape(1,-1), user_game.loc[user].values.reshape(1, -1))
  user_game['cos similarity'][user]=cos
sim_user = user_game[user_game['cos similarity'].astype(int) != 1]['cos similarity'].sort_values(ascending=False).head(15).index.to_list()
sim_games = df[df['UserID'].isin(sim_user)]['Game'].unique().tolist()
user_games = df[(df['UserID']==5250) & (df['Game'].isin(sim_games))]['Game'].unique().tolist()
recom_games = list(set(sim_games) - set(user_games))