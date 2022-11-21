branches=$(git for-each-ref --format='%(refname:short)' refs/remotes/origin | grep -v /HEAD | grep -v /master)

for branch in $branches;do
	declare x=${branch#origin/}
	echo "$x"
	if $x == "final-submission"; then
		continue
	fi
	git checkout $x
	mkdir ~/code_stuff/TempOx/$x
	rsync -av --exclude=".*" ~/code_stuff/SmartOx ~/code_stuff/TempOx/$x
done
