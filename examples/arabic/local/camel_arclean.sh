data_dir=/mgData4/yangb/data/MASC/masc

echo "clean dev/test Arbic text"
cd $data_dir/subsets
for f in clean_dev.csv clean_test.csv noisy_dev.csv noisy_test.csv; do
    camel_arclean $f -o camel_arclean_$f
done
echo "clean train Arbic text"
for f in `ls $data_dir/subtitles`; do
    camel_arclean $data_dir/subtitles/$f -o $data_dir/subtitles/camel_arclean_$f
done
