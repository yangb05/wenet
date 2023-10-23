wavedata=/mgData4/yangb/data/Arabic/wavedata
if [ ! -d "$wavedata" ]; then
    mkdir -p $wavedata
else
    rm -rf $wavedata
    mkdir -p $wavedata
fi

cd $wavedata
# link with mgb2 wavedata
ln -s ../../MGB_Arabic/wavedata/train_mer20 mgb2_train
ln -s ../../MGB_Arabic/wavedata/test_mer20 mgb2_test
# link with masc wavedata
ln -s ../../MASC/masc/wavedata/clean_train masc_clean_train
ln -s ../../MASC/masc/wavedata/noisy_train masc_noisy_train
ln -s ../../MASC/masc/wavedata/clean_dev masc_clean_dev
ln -s ../../MASC/masc/wavedata/noisy_dev masc_noisy_dev
ln -s ../../MASC/masc/wavedata/clean_test masc_clean_test
ln -s ../../MASC/masc/wavedata/noisy_test masc_noisy_test
# link with gale_p4_ara_bn_speech wavedata
ln -s ../untar/gale_p4_ara_bn_speech/wavedata gale_p4_ara_bn_speech
# link with Tunisian_MSA
ln -s ../untar/Tunisian_MSA/data/wavedata tunisian_msa