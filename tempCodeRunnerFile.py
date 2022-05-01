ete()
cnt = 0
mx=res[0][1]
for x in res:
    cnt += 1
    print(cnt)
    models.figd.objects.create(
        id=cnt,
        gene=x[0],
        number=x[1]/mx,
        level=level[x[0]]
    )
