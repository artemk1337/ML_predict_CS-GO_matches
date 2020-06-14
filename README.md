# ML_predict_CS-GO_matches

### data format:
-	match_url text,<br />
-	team1_url text,<br />
-	team2_url text,<br />


# The unofficial HLTV Python API

## INSTALLATION


## USAGE


```
>>> get_results_url(filename=None, pages_with_results=[0])
```
> __type: func__ <br />
> Params:
> - *filename* - for saving pandas frame <br />
> - *pages_with_results* - array with numbers of pages with results <br />
>
> Return pandas DataFrame with columns:
> - match_url <br />


```
>>> MatchPageParams(df, start_index=None, finish_index=None)
```
> __type: class__ <br />
> Params:
> - *df* - pandas frame with match urls
> - *start_index* - start index 
> - *finish_index* - alast index

```
>>> add_all_params()
```
> __type: def__ <br />
> Modify pandas frame, add columns:
> - *match_url* - link to the match
> - *event_url* - link to the tournament
> - *players_url_1* - links to players of the 1st team
> - *players_url_2* - links to players of the second team
> - *maps_url* - links to statistics of played maps
> - *maps_name* - map names
> - *score1_maps* - score on each map of team 1
> - *score2_maps* - score on each map of team 2
> - *picks* - peaks of teams; 1 - the first team, -1 - the second team; if the array is None, then the maps are <2
> - *date* - match date
> - *total_maps* - in total it was planned to play cards (usually 1, 3 or 5)
> - *maps_played* - how many cards were played as a result
> - *score1* - score of the 1st team
> - *score2* - score of the 2nd team
> - *h2h_wins1* - history of victories of the 1st team over the 2nd
> - *h2h_wins2* - the history of victories of the 2nd team over the 1st
> - *rank1* - rank of the 1st team
> - *rank2* - rank of the 2nd team











