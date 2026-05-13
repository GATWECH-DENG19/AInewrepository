% =========================
% BIDIRECTIONAL CONNECTIONS
% =========================
link(giorgis, fasilo).
link(giorgis, tana_shore).
link(giorgis, stadium).
link(giorgis, market).
link(giorgis, bdu_main).
link(giorgis, gish_abay).
link(giorgis, meskel_square).

link(fasilo, stadium).
link(stadium, market).
link(market, bdu_main).
link(tana_shore, kidane_meheret).
link(kidane_meheret, bdu_main).
link(bdu_main, polytechnic).
link(polytechnic, shumabo).
link(shumabo, abay_bridge).
link(abay_bridge, bezawit).
link(bezawit, zuria).
link(zuria, airport).
link(airport, hidase).
link(hidase, giorgis).
link(gish_abay, peda_campus).
link(peda_campus, meskel_square).
link(meskel_square, lemat).
link(lemat, zuria).
link(technology_campus, polytechnic).
link(technology_campus, shumabo).
link(medicine_campus, stadium).

% Bidirectional Rule
connected(X, Y) :- link(X, Y).
connected(X, Y) :- link(Y, X).

% =========================
% COORDINATES (20 Locations)
% =========================
coord(giorgis, 11.5936, 37.3908).
coord(fasilo, 11.5950, 37.3850).
coord(stadium, 11.5845, 37.3829).
coord(market, 11.5930, 37.3855).
coord(tana_shore, 11.6050, 37.3750).
coord(bdu_main, 11.5972, 37.3958).
coord(polytechnic, 11.5850, 37.3830).
coord(technology_campus, 11.5800, 37.4000).
coord(shumabo, 11.5800, 37.3820).
coord(abay_bridge, 11.6000, 37.4050).
coord(airport, 11.6010, 37.3210).
coord(gish_abay, 11.5900, 37.3900).
coord(meskel_square, 11.6060, 37.3920).
coord(zuria, 11.6020, 37.3800).
coord(bezawit, 11.6150, 37.4100).
coord(kidane_meheret, 11.5940, 37.4020).
coord(lemat, 11.6100, 37.3900).
coord(hidase, 11.5920, 37.3750).
coord(peda_campus, 11.6120, 37.3880).
coord(medicine_campus, 11.5800, 37.3790).

% =========================
% A* SEARCH LOGIC
% =========================
distance(A, B, D) :-
    coord(A, X1, Y1),
    coord(B, X2, Y2),
    D is sqrt((X1 - X2)^2 + (Y1 - Y2)^2).

edge_cost(X, Y, Cost) :- connected(X, Y), distance(X, Y, Cost).
heuristic(Node, Goal, H) :- distance(Node, Goal, H).

astar(Start, Goal, FinalPath, Cost) :-
    heuristic(Start, Goal, H),
    astar_search([[Start, 0, H, [Start]]], Goal, PathInverted, Cost),
    reverse(PathInverted, FinalPath).

astar_search([[Goal, G, _, Path] | _], Goal, Path, G).
astar_search([[Node, G, _, Path] | Rest], Goal, FinalPath, FinalCost) :-
    findall([Next, G2, F2, [Next | Path]],
        (connected(Node, Next), \+ member(Next, Path), 
         edge_cost(Node, Next, S), G2 is G + S, 
         heuristic(Next, Goal, H), F2 is G2 + H),
        Children),
    append(Rest, Children, Open),
    sort_open(Open, Sorted),
    astar_search(Sorted, Goal, FinalPath, FinalCost).

sort_open(L, S) :- map_list_to_pairs(get_f, L, P), keysort(P, SP), pairs_values(SP, S).
get_f([_, _, F, _], F).