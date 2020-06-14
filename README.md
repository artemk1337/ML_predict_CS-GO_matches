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
> Params: <br />
> - *filename* - for saving pandas frame <br />
> - *pages_with_results* - array with numbers of pages with results <br />
>
> Return pandas DataFrame with columns: <br />
> - match_url <br />


```
>>> MatchPageParams(df, start_index=None, finish_index=None)
```
> __type: class__ <br />
> Params: <br />
> - *df* - pandas frame with match urls
> - *start_index* - start index <br />
> - *finish_index* - alast index <br />
>









