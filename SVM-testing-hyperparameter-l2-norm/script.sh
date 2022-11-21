git fetch --all --prune

branches=$(git for-each-ref --format='%(refname:short)' refs/remotes/origin | grep -v /HEAD | grep -v /master)

for x in $branches;do
	#echo $branch
	declare branch=${x#origin/}
	echo "$branch"
	git checkout $branch
	mkdir /home/ayushmaankaushik/code_stuff/SmartOx-temp/$branch
	cp -r /home/ayushmaankaushik/code_stuff/SmartOx/. /home/ayushmaankaushik/code_stuff/SmartOx-temp/$branch	
done
