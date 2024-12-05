#!/usr/bin/env python3

#############################################################
##### RNASeq Analysis Pipeline with STAR                #####
##### Last update: 11/15/2022 Serdar Turkarslan         #####
##### Institute for Systems Biology                     #####
############################################################
import glob, sys, os, string, datetime, re
import argparse
import subprocess

from .find_files import find_fastq_files
from .trim_galore import trim_galore, collect_trimmed_data, create_result_dirs

DESCRIPTION = """run_STAR_SALMON.py - run STAR and Salmon"""

####################### Run STAR #####################################
### We need to add Read GRoup info
### --outSAMattrRGline ID:${i%_TF_R1_val_1.fq.gz}
### https://github.com/BarshisLab/danslabnotebook/blob/main/CBASSAS_GenotypeScreening.md

def run_star(first_pair_group, second_pair_group, results_dir, folder_name,
             genome_dir, is_gzip, args):
    print('\033[33mRunning STAR! \033[0m', flush=True)
    outfile_prefix = '%s/%s_%s_' % (results_dir, folder_name, args.starPrefix)
    star_options = ["--runThreadN", str(args.runThreadN),
                    "--outFilterType", "Normal",
                    "--outSAMstrandField", "intronMotif",
                    "--outFilterIntronMotifs", "RemoveNoncanonical",
                    "--outSAMtype", "BAM", "Unsorted",
                    "--limitBAMsortRAM", str(args.limitBAMsortRAM)]
    if is_gzip:
        star_options.extend(["--readFilesCommand", "zcat"])
    star_options.extend(["--outReadsUnmapped", "Fastx",
                         "--outFilterMismatchNmax", str(args.outFilterMismatchNmax),
                         "--outFilterMismatchNoverLmax", str(args.outFilterMismatchNoverLmax),
                         "--outFilterScoreMinOverLread", str(args.outFilterScoreMinOverLread),
                         "--outFilterMatchNmin", str(args.outFilterMatchNmin)])

    genome_load = "LoadAndKeep"  # This is the default, for efficiency
    if args.twopassMode:
        star_options.extend(["--twopassMode", "Basic"])
        genome_load = "NoSharedMemory"  # two-pass has to run without shared memory

    command = ["STAR", "--genomeDir", genome_dir]
    command += star_options
    if args.outSAMattributes != "Standard" and len(args.outSAMattributes) > 0:
        out_sam_attrs = args.outSAMattributes.split()
        command.append('--outSAMattributes')
        command += out_sam_attrs

    # Handling for GFF files
    if not args.genome_gff is None and os.path.exists(args.genome_gff):
        genome_load = "NoSharedMemory"  # can't use GFF with a shared genome memory
        gff_args = [
            '--sjdbGTFfile', args.genome_gff,
            '--sjdbGTFtagExonParentTranscript', args.sjdbGTFtagExonParentTranscript,
            '--limitSjdbInsertNsj', str(args.limitSjdbInsertNsj)
        ]
        if args.sjdbOverhang is not None:
            gff_args += ['--sjdbOverhang', str(args.sjdbOverhang)]
        command += gff_args

    command += [ "--readFilesIn", first_pair_group,
                 second_pair_group,
                 "--outFileNamePrefix", outfile_prefix]
    command += ["--genomeLoad", genome_load]

    # add more optional arguments
    if args.sjdbGTFfeatureExon is not None:
        command += ["--sjdbGTFfeatureExon", args.sjdbGTFfeatureExon]
    if args.sjdbGTFtagExonParentGene is not None:
        command += ["--sjdbGTFtagExonParentGene", args.sjdbGTFtagExonParentGene]
    if args.quantMode is not None:
        command += ["--quantMode"] + args.quantMode

    cmd = ' '.join(command)
    compl_proc = subprocess.run(command, check=True, capture_output=False, cwd=results_dir)

####################### Samtools sorting and indexing ##########
#
def run_samtools_sort_and_index(results_dir):
    bam_files = glob.glob(os.path.join(results_dir, "*.bam"))
    if len(bam_files) == 0:
        print("ERROR: could not sort and index - bam file not found")
        return
    sorted_bam_path = None
    for f in bam_files:
        if f.endswith("Sorted.out.bam"):
            sorted_bam_path = f

    filename = os.path.basename(bam_files[0])
    if sorted_bam_path is None:
        print("Using samtools to sort STAR BAM result")
        stem = bam_files[0].replace(".bam", "").replace(".out", "")
        sorted_bam_path = os.path.join(results_dir, "%s_Sorted.out.bam" % stem)
        command = ['samtools', 'sort', bam_files[0], '-o',
                   sorted_bam_path]
        compl_proc = subprocess.run(command, check=True,
                                    capture_output=False, cwd=results_dir)
    if not os.path.exists(sorted_bam_path + ".bai"):
        print("Using samtools to index sorted STAR BAM result")
        command = ["samtools", "index", sorted_bam_path]
        compl_proc = subprocess.run(command, check=True,
                                    capture_output=False, cwd=results_dir)


####################### Deduplication (not in _old) ###############################
def dedup(results_dir,folder_name):
    print('\033[33mRunning Deduplication! \033[0m', flush=True)
    outfile_prefix = '%s/%s_%s_' %(results_dir, folder_name, args.starPrefix)

    aligned_bam = '%sAligned.out.bam' % (outfile_prefix)
    fixmate_bam = '%sFixmate.out.bam' % (outfile_prefix)
    ordered_bam = '%sOrdered.out.bam' % (outfile_prefix)
    markdup_bam = '%sMarkedDup.out.bam' % (outfile_prefix)
    markdupSTAR_bam = '%sProcessed.out.bam' % (outfile_prefix)
    nosingleton_bam = '%sNoSingleton.out.bam' % (outfile_prefix)
    nosingletonCollated_bam = '%sNoSingletonCollated.out.bam' % (outfile_prefix)

    # STAR mark duplicates
    star_markdup_command = ['STAR', '--runThreadN', '32',
                            '--runMode',
                            'inputAlignmentsFromBAM',
                            '--bamRemoveDuplicatesType', 'UniqueIdenticalNotMulti',
                            '--inputBAMfile', aligned_bam,
                            '--outFileNamePrefix', outfile_prefix]
    star_markdup_cmd = ' '.join(star_markdup_command)

    # removesingletons from STAR
    rmsingletonsSTAR_command = ['samtools', 'view', '-@', '8',
                                '-b', '-F', '0x400', markdupSTAR_bam,
                                '>', nosingleton_bam]
    rmsingletonsSTAR_cmd = ' '.join(rmsingletonsSTAR_command)

    # Collate reads by name
    collatereadsSTAR_command = ['samtools', 'sort', '-o',
                                nosingletonCollated_bam,
                                '-n', '-@', '8', nosingleton_bam]
    collatereadsSTAR_cmd = ' '.join(collatereadsSTAR_command)

    ## STAR based BAM duplicate removal
    # Mark duplicates with STAR
    print('STAR mark duplicates run command:%s' % star_markdup_cmd, flush=True)
    compl_proc = subprocess.run(star_markdup_command, check=True, capture_output=False, cwd=results_dir)

    # Remove marked duplicates withh samtools
    print('Samtools  STAR Dedup Remove run command:%s' % rmsingletonsSTAR_cmd, flush=True)
    compl_proc = subprocess.run(rmsingletonsSTAR_cmd, shell=True, check=True, capture_output=False, cwd=results_dir)

    # Remove marked duplicates withh samtools
    print('Samtools  Collate reads by read name run command:%s' % collatereadsSTAR_cmd, flush=True)
    compl_proc = subprocess.run(collatereadsSTAR_cmd, shell=True, check=True, capture_output=False, cwd=results_dir)


####################### Run Salmon Count ###############################
# WW: Check the names of the input files they will be different from _out
def run_salmon_quant(results_dir, folder_name, genome_fasta):
    outfile_prefix = '%s/%s_%s_' %(results_dir, folder_name, args.starPrefix)
    print(outfile_prefix, flush=True)
    print('\033[33mRunning salmon-quant! \033[0m', flush=True)
    # check if we are performing deduplication
    if args.dedup:
        salmon_input = '%sNoSingletonCollated.out.bam' % (outfile_prefix)
    else:
        salmon_input = '%sAligned.out.bam' % (outfile_prefix)

        # Use BAM file aligned to transcriptome for salmon input if it exists
        salmon_transcriptome_input = "%sAligned.toTranscriptome.out.bam" % outfile_prefix
        if os.path.exists(salmon_transcriptome_input):
            salmon_input = salmon_transcriptome_input

    command = ['salmon', 'quant', '-t', genome_fasta,
        '-l', 'A',  '-a',  salmon_input, '-o', '%s/%s_salmon_quant' % (results_dir, args.salmonPrefix)]
    cmd = ' '.join(command)
    print("Salmon quant command: '%s'" % cmd, flush=True)
    # run as a joined string
    compl_proc = subprocess.run(cmd, check=True, capture_output=False, cwd=results_dir, shell=True)


####################### Run HTSEq Count ###############################
#### We can remove this since we are using salmon quant
def run_htseq(htseq_dir, results_dir, folder_name, genome_gff):
    print('\033[33mRunning htseq-count! \033[0m', flush=True)
    htseq_input = '%s/%s_star_Aligned.sortedByCoord.out.bam' %(results_dir, folder_name)
    cmd = 'htseq-count -s "reverse" -t "exon" -i "Parent" -r pos --max-reads-in-buffer 60000000 -f bam %s %s > %s/%s_htseqcounts.txt' %(htseq_input,
                                                                                                                                        genome_gff,htseq_dir,folder_name)
    print('htseq-count run command: %s' % cmd, flush=True)
    os.system(cmd)


####################### Running the Pipeline ###############################

def run_pipeline(data_folder, results_folder, genome_dir, genome_fasta, args):
    folder_count = 1

    # Loop through each data folder
    folder_name = data_folder.split('/')[-1]
    print('\033[33mProcessing Folder: %s\033[0m' % folder_name, flush=True)

    # Get the list of first file names in paired end sequences
    ## We need to make sure we capture fastq data files
    pair_files = find_fastq_files(data_folder, args.fastq_patterns.split(','))

    # Program specific results directories
    data_trimmed_dir = "%s/%s/trimmed" % (results_folder,folder_name)
    fastqc_dir = "%s/%s/fastqc_results" % (results_folder,folder_name)

    results_dir = "%s/%s/results_STAR_Salmon" %(results_folder, folder_name)
    htseq_dir = "%s/htseqcounts" % (results_dir)

    # Run create directories function to create directory structure
    create_result_dirs(data_trimmed_dir, fastqc_dir, results_dir, htseq_dir)

    print("PAIR_FILES: ", pair_files, flush=True)

    # Loop through each file and create filenames
    file_count = 1

    is_gzip = True
    is_paired_end = True

    for pair_file in pair_files:
        first_pair_file, second_pair_file = pair_file
        if second_pair_file is None:
            is_paired_end = False

        fastq_fname = os.path.basename(first_pair_file)
        is_gzip = fastq_fname.endswith("gz")
        if is_gzip:
            file_ext = '.'.join(fastq_fname.split('.')[-2:])
        else:
            file_ext = fastq_fname.split('.')[-1]

        print('\033[32m Processing file set: %s of %s (first is "%s")\033[0m' % (file_count, len(pair_files),
                                                                                 first_pair_file),
              flush=True)

        # Collect Sample attributes
        sample_id = fastq_fname.replace(file_ext, "")
        print("sample_id: %s" % sample_id, flush=True)

        # Run TrimGalore
        trim_galore(first_pair_file, second_pair_file, folder_name,sample_id, data_trimmed_dir, fastqc_dir)
        file_count += 1

    # Collect Trimmed data for input into STAR
    first_pair_group, second_pair_group = collect_trimmed_data(data_trimmed_dir, is_gzip, is_paired_end)

    # Run STAR
    run_star(first_pair_group, second_pair_group, results_dir, folder_name, genome_dir, is_gzip, args)

    # Run samtools, sorting and indexing
    run_samtools_sort_and_index(results_dir)

    # Run Deduplication
    if args.dedup:
        print('\033[33mRunning Deduplication: \033[0m', flush=True)
        dedup(results_dir,folder_name)

    # Run Salmon Quant
    if args.salmon_genome_fasta is not None:
        genome_fasta = args.salmon_genome_fasta

    run_salmon_quant(results_dir, folder_name, genome_fasta)
    folder_count += 1

    return data_trimmed_dir, fastqc_dir, results_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=DESCRIPTION)
    parser.add_argument('genomedir', help='genome directory')
    parser.add_argument('dataroot', help="parent of input directory")
    parser.add_argument('indir', help="input directory (R<somenumber>)")
    parser.add_argument('outdir', help='output directory')
    parser.add_argument('--fastq_patterns', help="FASTQ file patterns", default="*_{{pairnum}}.fq.*")
    parser.add_argument('--genome_gff', help='genome GFF file')
    parser.add_argument('--genome_fasta', help='genome FASTA file')
    parser.add_argument('--dedup', action='store_true', help='should we deduplicate bam files (True or False)')
    parser.add_argument('--twopassMode', action='store_true', help='run STAR in two-pass mode')
    parser.add_argument('--starPrefix', help="STAR output file name prefix")
    parser.add_argument('--salmonPrefix', help="Salmon output folder name prefix")
    parser.add_argument('--outFilterMismatchNmax', nargs='?', const=10, type=int)
    parser.add_argument('--outFilterMismatchNoverLmax', nargs='?', const=0.3, type=float)
    parser.add_argument('--outFilterScoreMinOverLread', nargs='?', const=0.66, type=float)
    parser.add_argument('--outFilterMatchNmin', nargs='?', const=0, type=int)
    parser.add_argument('--outSAMattributes', nargs='?', type=str, default="Standard")
    parser.add_argument('--runThreadN', type=int, default=32)
    parser.add_argument('--limitBAMsortRAM', type=int, default=5784458574)
    parser.add_argument('--sjdbGTFtagExonParentTranscript', default="Parent")
    parser.add_argument('--sjdbOverhang', type=int, default=None)
    parser.add_argument('--limitSjdbInsertNsj', type=int, default=1602710)

    parser.add_argument('--sjdbGTFfeatureExon')
    parser.add_argument('--sjdbGTFtagExonParentGene')
    parser.add_argument('--quantMode', nargs="+")
    parser.add_argument('--salmon_genome_fasta')

    args = parser.parse_args()

    now = datetime.datetime.now()
    timeprint = now.strftime("%Y-%m-%d %H:%M")
    data_folder = "%s/%s" % (args.dataroot, args.indir)
    if args.genome_fasta is not None and os.path.exists(args.genome_fasta):
        genome_fasta = args.genome_fasta
    else:
        genome_fasta = glob.glob('%s/*.fasta' % (args.genomedir))[0]

    data_trimmed_dir,fastqc_dir,results_dir = run_pipeline(data_folder, args.outdir, args.genomedir, genome_fasta, args)
