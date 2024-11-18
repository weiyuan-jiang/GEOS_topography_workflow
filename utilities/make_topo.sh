#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --constraint=cas
#SBATCH --ntasks-per-node=45
#SBATCH --job-name=make_topo
#SBATCH --account=s1873
#SBATCH --mail-type=ALL

export mypath=`readlink -f $0`
export topo_bin=`dirname $mypath`
source $topo_bin/g5_modules.sh

export output_dir=$1
export   work_dir=$2
shift 2


for n in $@;
do

   if [[ ! -e $output_dir ]]; then
      mkdir $output_dir
   fi 
   if [[ ! -e $work_dir ]]; then
      mkdir $work_dir
   fi

   cd $work_dir

   config_file=GenScrip.rc
   let jm=$n*6
   echo $n
   echo $jm
   scripfile=PE${n}x${jm}-CF.nc4
   echo $scripfile
   echo $config_file
   cat << _EOF_ > ${config_file}
CUBE_DIM: $n
output_scrip: ${scripfile}
output_geos: c${n}_coords.nc4
_EOF_
   mpirun -np 6 ${topo_bin}/generate_scrip_cube.x
   rm GenScrip.rc

   cd $output_dir
   echo "running c$n"
   ${topo_bin}/run_topo_generation.py --res $n --hres_topo /discover/nobackup/bmauer/gmted_topo/gmted_fix_superior/gmted_fixed_anartica_superior_caspian.nc4 --outputdir $output_dir --topo_install $topo_bin --workdir $work_dir

done

