****************************************************************************
``sistr_cmd``: Salmonella In Silico Typing Resource (SISTR) commandline tool
****************************************************************************

|pypi| |nbsp| |license| |nbsp| |galaxy| |nbsp| |render|

.. |pypi| image:: https://badge.fury.io/py/sistr-cmd.svg
    :target: https://pypi.python.org/pypi/sistr-cmd/
.. |license| image:: https://img.shields.io/github/license/phac-nml/sistr_cmd
	:target: https://www.apache.org/licenses/LICENSE-2.0
.. |galaxy| image:: https://img.shields.io/badge/usegalaxy-.eu-brightgreen
	:target: https://usegalaxy.eu/root?tool_id=sistr_cmd	
.. |nbsp| unicode:: 0xA0 
   :trim:
.. |render| image:: https://img.shields.io/badge/render.com-deployed-brightgreen
   :target: https://sistr-app.onrender.com/
   :alt: web app deployed on Render.com Cloud Hosting

*Salmonella* serovar predictions from whole-genome sequence assemblies by determination of antigen gene and cgMLST gene alleles using BLAST.
`Mash MinHash <https://mash.readthedocs.io/en/latest/>`_ can also be used for serovar prediction.

.. epigraph::

	`Latest stable version <https://github.com/phac-nml/sistr_cmd/releases/latest>`_


*Don't want to use a command-line app?* Try SISTR with interface deployed on Galaxy and Render.com online platforms (see the `Web application`_ section)  


Citation
========

If you find this tool useful, please cite as:

.. epigraph::

	The *Salmonella In Silico* Typing Resource (SISTR): an open web-accessible tool for rapidly typing and subtyping draft *Salmonella* genome assemblies. Catherine Yoshida, Peter Kruczkiewicz, Chad R. Laing, Erika J. Lingohr, Victor P.J. Gannon, John H.E. Nash, Eduardo N. Taboada. PLoS ONE 11(1): e0147101. doi: 10.1371/journal.pone.0147101

	-- Paper Link: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0147101

BibTeX
------

.. code-block:: none

	@article{Yoshida2016,
		doi = {10.1371/journal.pone.0147101},
		url = {http://dx.doi.org/10.1371/journal.pone.0147101},
		year  = {2016},
		month = {jan},
		publisher = {Public Library of Science ({PLoS})},
		volume = {11},
		number = {1},
		pages = {e0147101},
		author = {Catherine E. Yoshida and Peter Kruczkiewicz and Chad R. Laing and Erika J. Lingohr and Victor P. J. Gannon and John H. E. Nash and Eduardo N. Taboada},
		editor = {Michael Hensel},
		title = {The Salmonella In Silico Typing Resource ({SISTR}): An Open Web-Accessible Tool for Rapidly Typing and Subtyping Draft Salmonella Genome Assemblies},
		journal = {{PLOS} {ONE}}
	}



Installation
============

Using Conda [Recommended]
---------------------------

You can install ``sistr_cmd`` using `Conda <https://conda.io/miniconda.html>`_ from the `BioConda channel <https://bioconda.github.io/>`_:

.. code-block:: bash

	# Install conda. Miniconda is recommended if you don't have Conda installed already
	# see https://conda.io/miniconda.html
	# Add Bioconda channel and other channels https://bioconda.github.io/#set-up-channels
	conda config --add channels conda-forge
	conda config --add channels defaults
	conda config --add channels r
	conda config --add channels bioconda
	# Install sistr_cmd and its dependencies
	conda install sistr_cmd
	# sistr_cmd should be installed in your $PATH
	sistr --help

Installing ``sistr_cmd`` is recommended for the least amount of headache since Conda will ensure that all necessary external dependencies are installed along with ``sistr_cmd`` (i.e. ``blast+``, ``mafft``, ``mash``). This will also help you get ``sistr_cmd`` running on older systems (e.g. CentOS 5) or where you may not have many user privileges. 


Using ``pip``
-------------

You can install ``sistr_cmd`` using ``pip``:

.. code-block:: bash

	pip install sistr_cmd


``sistr_cmd`` is available from PYPI at https://pypi.python.org/pypi/sistr-cmd

**NOTE:** You will need to ensure that external dependencies are installed (i.e. ``blast+``, ``mafft``, ``mash`` [optionally])

Using ``setup.py``
------------------
You can install ``sistr_cmd`` directly from the source code:

.. code-block:: bash

	python setup.py install

**NOTE:** If you run into ``pycurl`` library installation issues, you can try to resolve them by installing system dependencies via a package manager such as ``apt`` (``apt install python3-pycurl libcurl4-openssl-dev libssl-dev``)

Web application
---------------
SISTR can be publically accessed as a web application via:

- Galaxy EU instance at https://usegalaxy.eu/root?tool_id=sistr_cmd |galaxy|
- Render.com Cloud Hosting Platform-as-a-Service (PaaS) hosts a **DEMO** SISTR web application https://sistr-app.onrender.com/ |render|

**NOTE 1:** The SISTR web application hosted on Render.com might take up to 20 seconds to load on the first run and will shutdown after 15 min of inactivity

**NOTE 2:** SISTR web application source code is available at https://github.com/phac-nml/sistr-web-app allowing easy web interface deployment on any infrastructure types (on-premises, cloud/remote). 


Database
=========
SISTR will automatically initialize database of *Salmonella* serovar determination antigens, cgMLST profiles and MASH sketch of reference genomes by downloading it from a remote location. 
The SISTR database v1.3 got minor updates by collapsing some of the serovars with O24/O25 antigens detailed in `CHANGELOG.md <CHANGELOG.md>`_ file

- SISTR v1.1 database is available at https://zenodo.org/records/13618515 or via a direct url https://zenodo.org/records/13618515/files/SISTR_V_1.1_db.tar.gz?download=1  (used with SISTR < 1.1.3 )
- SISTR v1.3 database is available at https://zenodo.org/records/14270992 or va a direct url https://zenodo.org/records/14270992/files/SISTR_V_1.1.3_db.tar.gz?download=1 (used with SISTR >= 1.1.3)


Dependencies
============

These are the external dependencies required for ``sistr_cmd``:

- Python (>= v2.7 OR >= v3.4)
- BLAST+ (>= v2.2.30)
- MAFFT (>=v7.271 (2016/1/6))
- `Mash v2.0+ <https://github.com/marbl/Mash/releases>`_ [optional]

Python Dependencies
-------------------

``sistr_cmd`` requires the following Python libraries:

- numpy (>=1.11.1)
- pandas (>=0.18.1)


You can run the following commands to get up-to-date versions of ``numpy`` and ``pandas``

.. code-block:: bash

	pip install --upgrade pip
	pip install wheel
	pip install numpy pandas

Usage
=====

If you run ``sistr -h``, you should see the following usage info:

.. code-block:: none

	usage: sistr_cmd [-h] [-i fasta_path genome_name] [-f OUTPUT_FORMAT]
	                 [-o OUTPUT_PREDICTION] [-p CGMLST_PROFILES]
	                 [-n NOVEL_ALLELES] [-a ALLELES_OUTPUT] [-T TMP_DIR] [-K]
	                 [--use-full-cgmlst-db] [--no-cgmlst] [-m] [--qc] [-t THREADS]
	                 [-v] [-V]
	                 [F [F ...]]

	SISTR (Salmonella In Silico Typing Resource) Command-line Tool
	==============================================================
	Serovar predictions from whole-genome sequence assemblies by determination of antigen gene and cgMLST gene alleles using BLAST.

	Note about using the "--use-full-cgmlst-db" flag:
	The "centroid" allele database is ~10% the size of the full set so analysis is much quicker with the "centroid" vs "full" set of alleles. Results between 2 cgMLST allele sets should not differ.

	If you find this program useful in your research, please cite as:

	The Salmonella In Silico Typing Resource (SISTR): an open web-accessible tool for rapidly typing and subtyping draft Salmonella genome assemblies.
	Catherine Yoshida, Peter Kruczkiewicz, Chad R. Laing, Erika J. Lingohr, Victor P.J. Gannon, John H.E. Nash, Eduardo N. Taboada.
	PLoS ONE 11(1): e0147101. doi: 10.1371/journal.pone.0147101

	positional arguments:
	  F                     Input genome FASTA file

	optional arguments:
	  -h, --help            show this help message and exit
	  -i fasta_path genome_name, --input-fasta-genome-name fasta_path genome_name
	                        fasta file path to genome name pair
	  -f OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
	                        Output format (json, csv, pickle)
	  -o OUTPUT_PREDICTION, --output-prediction OUTPUT_PREDICTION
	                        SISTR serovar prediction output path
	  -p CGMLST_PROFILES, --cgmlst-profiles CGMLST_PROFILES
	                        Output CSV file destination for cgMLST allelic
	                        profiles
	  -n NOVEL_ALLELES, --novel-alleles NOVEL_ALLELES
	                        Output FASTA file destination of novel cgMLST alleles
	                        from input genomes
	  -a ALLELES_OUTPUT, --alleles-output ALLELES_OUTPUT
	                        Output path of allele sequences and info to JSON
	  -T TMP_DIR, --tmp-dir TMP_DIR
	                        Base temporary working directory for intermediate
	                        analysis files.
	  -K, --keep-tmp        Keep temporary analysis files.
	  --use-full-cgmlst-db  Use the full set of cgMLST alleles which can include
	                        highly similar alleles. By default the smaller
	                        "centroid" alleles or representative alleles are used
	                        for each marker.
	  --no-cgmlst           Do not run cgMLST serovar prediction
	  -m, --run-mash        Determine Mash MinHash genomic distances to Salmonella
	                        genomes with trusted serovar designations. Mash binary
	                        must be in accessible via $PATH (e.g. /usr/bin).
	  --qc                  Perform basic QC to provide level of confidence in
	                        serovar prediction results.
	  -t THREADS, --threads THREADS
	                        Number of parallel threads to run sistr_cmd analysis.
	  -l LIST_OF_SEROVARS, --list-of-serovars LIST_OF_SEROVARS
                        	A path to a single column text file containing list of
                        	serovar(s) to check serovar prediction against. Result
                        	reported in the "predicted_serovar_in_list"
                        	field as Y (present) or N (absent) value.
	  -v, --verbose         Logging verbosity level (-v == show warnings; -vvv ==
	                        show debug info)
	  -V, --version         show program's version number and exit


Example Usage
-------------

By running the following command on a FASTA file of *Salmonella enterica* strain LT2 (https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP014051.1):

.. code-block:: bash

	sistr --qc -vv --alleles-output allele-results.json --novel-alleles novel-alleles.fasta --cgmlst-profiles cgmlst-profiles.csv -f tab -o sistr-output.tab LT2.fasta


You should see some log messages like so:

.. code-block:: none

	<time> INFO: Running sistr_cmd 0.3.4 [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:290]
	<time> INFO: Serial single threaded run mode on 1 genomes [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:319]
	<time> INFO: Initializing temporary analysis directory "/tmp/20170309104912-SISTR-LT2" and preparing for BLAST searching. [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:175]
	<time> INFO: Temporary FASTA file copied to /tmp/20170309104912-SISTR-LT2/LT2_fasta [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:177]
	<time> INFO: Running BLAST on serovar predictive cgMLST330 alleles [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:319]
	<time> INFO: Reading BLAST output file "/tmp/20170309104912-SISTR-LT2/cgmlst-centroid.fasta-LT2_fasta-2017Mar09_10_49_13.blast" [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:322]
	<time> INFO: Found 6525 cgMLST330 allele BLAST results [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:333]
	<time> INFO: Marker NZ_AOXE01000081.1_201 | Recovered novel allele with gaps (n=0) of length 477 vs length 477 for ref allele NZ_AOXE01000081.1_201|2823059714. Novel allele name=3250876267 [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:181]
	<time> INFO: Type retrieved_marker_alleles <type 'dict'> [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:343]
	<time> INFO: Calculating number of matching alleles to serovar predictive cgMLST330 profiles [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:360]
	<time> INFO: Top subspecies by cgMLST is "enterica" (min dist=0.00909090909091, Counter={'enterica': 11532}) [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:369]
	<time> INFO: Top serovar by cgMLST profile matching: "Typhimurium" with 327 matching alleles, distance=0.9% [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:385]
	<time> INFO: cgMLST330 Sequence Type=660408169 [in /usr/lib/python2.7/site-packages/sistr/src/cgmlst/__init__.py:404]
	<time> INFO: LT2 | Antigen gene BLAST serovar prediction: "Typhimurium" serogroup=B 1,4,[5],12:i:1,2 [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:207]
	<time> INFO: LT2 | Subspecies prediction: enterica [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:210]
	<time> INFO: LT2 | Overall serovar prediction: Typhimurium [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:213]
	<time> INFO: Genome size=4857473 (within gsize thresholds? True) [in /usr/lib/python2.7/site-packages/sistr/src/qc/__init__.py:13]
	<time> INFO: Deleting temporary working directory at /tmp/20170309104912-SISTR-LT2 [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:220]
	<time> INFO: Writing output "tab" file to "sistr-output.tab" [in /usr/lib/python2.7/site-packages/sistr/src/writers.py:38]
	<time> INFO: cgMLST allelic profiles written to cgmlst-profiles.csv [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:340]
	<time> INFO: JSON of allele data written to allele-results.json for 1 cgMLST allele results [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:343]
	<time> INFO: Wrote 330 alleles to novel-alleles.fasta [in /usr/lib/python2.7/site-packages/sistr/sistr_cmd.py:346]


``sistr_cmd`` Output
====================

``sistr_cmd`` has several output options. The primary output is the serovar prediction and in silico typing results output (e.g. ``-o sistr-results.tab``).

Summary of output options:

- primary results output 
	+ serovar prediction, cgMLST results, Mash results
	+ format (``-f <format>``): ``tab``, ``csv``, ``json``, ``pickle``
	+ ``-o sistr-results``
- cgMLST allele results
	+ in-depth allele search results for each input genome for each cgMLST locus (330 loci in total)
	+ includes extracted allele sequences, top ``blastn`` results and summarized ``mafft`` results
	+ format: JSON
	+ ``-a allele-results.json``
- cgMLST allelic profiles
	+ table of allele designations for each genome for each cgMLST locus
	+ row names: genome names
	+ column names: cgMLST marker names
	+ format: CSV
	+ ``--cgmlst-profiles cgmlst-profiles.csv``


Primary results output (``-o sistr-results``)
---------------------------------------------
SISTR supports various text output formats specified by the ``-f`` option with ``json`` being the default.

JSON results output (``-f json``):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: json

	[
	  {
	    "serovar_cgmlst": "Typhimurium",
	    "cgmlst_matching_alleles": 327,
	    "h1": "i",
	    "serovar_antigen": "Typhimurium",
	    "cgmlst_distance": 0.009090909090909038,
	    "h2": "1,2",
	    "cgmlst_genome_match": "LT2",
	    "cgmlst_ST": 660408169,
	    "serovar": "Typhimurium",
	    "fasta_filepath": "/full/path/to/LT2.fasta",
	    "genome": "LT2",
	    "serogroup": "B",
	    "qc_messages": "",
	    "qc_status": "PASS",
	    "o_antigen": "1,4,[5],12",
	    "cgmlst_subspecies": "enterica"
	  }
	]


Tab-delimited results output (``-f tab``):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text
	
	cgmlst_ST	cgmlst_distance	cgmlst_genome_match	cgmlst_matching_alleles	cgmlst_subspecies	fasta_filepath	genome	h1	h2	o_antigen	qc_messages	qc_status	serogroup	serovar	serovar_antigen	serovar_cgmlst
	660408169	0.00909090909091	LT2	327	enterica	/home/peter/Downloads/sistr-LT2-example/LT2.fasta	LT2	i	1,2	1,4,[5],12		PASS	B	Typhimurium	Typhimurium	Typhimurium

CSV results output (``-f csv``):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Raw ``csv`` output results opened in a text editor

.. code-block:: csv

	cgmlst_ST,cgmlst_distance,cgmlst_genome_match,cgmlst_matching_alleles,cgmlst_subspecies,fasta_filepath,genome,h1,h2,o_antigen,qc_messages,qc_status,serogroup,serovar,serovar_antigen,serovar_cgmlst
	660408169,0.00909090909091,LT2,327,enterica,/home/peter/Downloads/sistr-LT2-example/LT2.fasta,LT2,i,"1,2","1,4,[5],12",,PASS,B,Typhimurium,Typhimurium,Typhimurium

The same ``csv`` results rendered as a table

.. csv-table:: 

	cgmlst_ST,cgmlst_distance,cgmlst_genome_match,cgmlst_matching_alleles,cgmlst_subspecies,fasta_filepath,genome,h1,h2,o_antigen,qc_messages,qc_status,serogroup,serovar,serovar_antigen,serovar_cgmlst
	660408169,0.00909090909091,LT2,327,enterica,/home/peter/Downloads/sistr-LT2-example/LT2.fasta,LT2,i,"1,2","1,4,[5],12",,PASS,B,Typhimurium,Typhimurium,Typhimurium


cgMLST allele search results
-------------------------------------

You can produce in-depth allele search results with the ``-a``/``--alleles-output`` commandline argument.
These results may be useful for understanding unexpected or low confidence serovar predictions.

Schema:
~~~~~~~

.. code-block:: text
	
	{
		<genome name>: {
			// for each 
			<cgMLST marker id>: {
				// top blast result on largest contig
				blast_result: {
					// perfect match to a previously identified allele?
					"is_perfect": boolean,
					// blastn subject sequence length
					"slen": integer,
					// blastn percent identity
					"pident": numeric,
					// cgMLST marker name
					"marker": string,
					// blastn query sequence id
					"qseqid": string,
					// blastn query sequence start index
					"qstart": integer,
					// is match truncated by end of sequence? 
					"is_trunc": boolean,
					// number of MSA gaps in subject sequence
					"sseq_msa_gaps": integer,
					// blastn subject sequence
					"sseq": string,
					// blastn bitscore
					"bitscore": numeric,
					// proportion of subject sequence MSA with gaps
					"sseq_msa_p_gaps": numeric,
					// blastn E-value
					"evalue": numeric,
					// blastn gap open
					"gapopen": integer,
					// blastn subject sequence end index
					"send": integer,
					// does this allele have a perfect match?
					"has_perfect_match": boolean,
					// matching allele name
					"allele": integer,
					// subject sequence start index
					"sstart": integer,
					// extracted allele name (CRC32 of subject nucleotide sequence)
					"allele_name": integer,
					// adjusted subject sequence start index
					"start_idx": numeric,
					// blastn query end index
					"qend": integer,
					// did the extracted allele sequence need to be reverse complemented?
					"needs_revcomp": boolean,
					// did the extracted allele sequence need to be extended to match the length of the query sequence?
					"is_extended": boolean,
					// blastn number of mismatches
					"mismatch": integer,
					// extracted allele coverage i.e. (length of extracted allele) / (length of closest matching allele)
					"coverage": numeric,
					// too many gaps within the MSA of extracted allele sequence and closest matching allele?
					"too_many_gaps": boolean,
					// adjusted subject end index
					"end_idx": numeric,
					// is extracted allele truncated by end of sequence? 
					"trunc": boolean,
					// blastn subject sequence title
					"stitle": string,
					// blastn query sequence length
					"qlen": integer,
					// valid allele match found?
					"is_match": true,
					// blastn alignment length
					"length": integer
				},
				// CRC32 unsigned 32-bit integer allele name from allele sequence
				"name": integer,
				// extracted allele sequence
				"seq": string
			}
			
		}
	}

Example:
~~~~~~~~

Here's some truncated example allele search results output in JSON format for ``LT2`` sample:

.. code-block:: text

	{
	  "LT2": {
	    "NZ_AOXE01000034.1_82": {
	      "blast_result": {
	        "is_perfect": false,
	        "slen": 4857473,
	        "pident": 99.479,
	        "marker": "NZ_AOXE01000034.1_82",
	        "qseqid": "NZ_AOXE01000034.1_82|340989631",
	        "qstart": 1,
	        "is_trunc": false,
	        "sseq_msa_gaps": 0,
	        "sseq": "ATGCCAACCAGACCACCTTATCCGCGGGAAGCTTATATCGTCACCATTGAAAAAGGCACGCCGGGCCAGACGGTGACGTGGTATCAGCTACGGGCTGACCATCCGAAACCTGATTCGCTCATCAGCGAGCATCCGACCGCAGAAGAAGCGATGGATGCGAAAAATCGTTACGAAGATCCGGATAAATCATAG",
	        "bitscore": 350.0,
	        "sseq_msa_p_gaps": 0.0,
	        "evalue": 3.289999999999999E-97,
	        "gapopen": 0,
	        "send": 358277,
	        "has_perfect_match": false,
	        "allele": 340989631,
	        "sstart": 358468,
	        "allele_name": 1204520418,
	        "start_idx": 358276.0,
	        "qend": 192,
	        "needs_revcomp": true,
	        "is_extended": false,
	        "mismatch": 1,
	        "coverage": 1.0,
	        "too_many_gaps": false,
	        "end_idx": 358467.0,
	        "trunc": false,
	        "stitle": "NZ_CP014051.1 Salmonella enterica strain LT2, complete genome",
	        "qlen": 192,
	        "is_match": true,
	        "length": 192
	      },
	      "name": 1204520418,
	      "seq": "ATGCCAACCAGACCACCTTATCCGCGGGAAGCTTATATCGTCACCATTGAAAAAGGCACGCCGGGCCAGACGGTGACGTGGTATCAGCTACGGGCTGACCATCCGAAACCTGATTCGCTCATCAGCGAGCATCCGACCGCAGAAGAAGCGATGGATGCGAAAAATCGTTACGAAGATCCGGATAAATCATAG"
	    },
	    // 329 other cgMLST allele results
	  },
	  "another-genome": { /* allele results */}
	}


cgMLST allelic profiles output (``--cgmlst-profiles cgmlst-profiles.csv``)
--------------------------------------------------------------------------

With the ``-p``/``--cgmlst-profiles`` commandline argument, you can output the 330 loci cgMLST allelic profiles for your input genomes (i.e. the allele designation for each cgMLST locus for each input genome). 
You can use this information to construct phylogenetic trees from this data using a tool such as `Phyloviz Online <https://online.phyloviz.net/index>`_ by uploading cgMLST profiles data. 
This type of analysis may be useful to explore why unexpected serovar prediction results were generated (e.g. your genomes are genetically very different from each other). 

Example truncated cgMLST profiles output:

.. csv-table::

	,NC_003198.1_3005,NC_006905.1_2841,NC_011149.1_467,...
	LT2,419666160,2853045644,161888011,...



QC by ``sistr_cmd`` (``--qc``)
------------------------------

If you are running ``sistr_cmd`` with the ``--qc`` commandline argument, ``sistr_cmd`` will run some basic QC to determine the level of confidence in the serovar prediction. 

The ``qc_status`` field should contain a value of ``PASS`` if your genome passes all QC checks, otherwise, it will be ``WARNING`` or ``FAIL`` if there are issues with your results and/or input genome sequence.

The ``qc_messages`` field will contain useful information about why you may have a low confidence serovar prediction result. The QC messages will be delimited by `` | `` symbol.

For example, here are the QC messages for an unusually small *Salmonella* assembly where the predicted serovar was "-:-:-":

.. code-block:: none

	FAIL: Large number of cgMLST330 loci missing (n=272 > 30)
	FAIL: Wzx/Wzy genes missing. Cannot determine O-antigen group/serogroup. Cannot accurately predict serovar from antigen genes.
	WARNING: H1 antigen gene (fliC) missing. Cannot determine H1 antigen. Cannot accurately predict serovar from antigen genes.
	WARNING: Input genome size (699860 bp) not within expected range of 4000000-6000000 (bp) for Salmonella
	WARNING: Only matched 57 cgMLST330 loci. Min threshold for confident serovar prediction from cgMLST is 297.0

The QC messages produced by ``sistr_cmd`` should help you understand your serovar prediction results.

Galaxy workflows
================
The `galaxy <./galaxy/>`_ folder contains Galaxy SISTR workflows that can be readily imported into existing Galaxy server instance and allow to process WGS samples in large batches starting from raw reads and finishing with serovar results.


- `Galaxy-Workflow-Assembly-Serotyping-withReport-for-SISTR_v1.1.1+galaxy1-recipe.ga <./galaxy/Galaxy-Workflow-Assembly-Serotyping-withReport-for-SISTR_v1.1.1+galaxy1-recipe.ga>`_
	+ Summary: Assembles genomes from raw reads, performs serotyping and generates overall report
	+ Uses tool dependencies: ``sistr 1.1.1+galaxy1``, ``shovill 1.0.4+galaxy1`` and ``tp_cat 0.1.0``


Issues
======

If you encounter any problems or have any questions feel free to create an issue anonymously or not to let us know so we can address it!

Feature requests and pull requests are welcome!


Want to help improve this tool?
===============================

Do you have any *Salmonella* genomes with trustworthy serovar info? Would you like SISTR to provide better serovar predictions? You can help by contributing those genomes along with their serovar info!

SISTR relies on a database of cgMLST allelic profiles from *Salmonella* genomes with validated serovar info to make accurate serovar predictions (since antigenic determinations from a handful of genes like wzx or fliC can only get you so far). So the more genomes there are in the SISTR database, the more accurate the serovar predictions, especially if those genomes belong to uncommon or rare serovars or lineages.

Help us improve SISTR serovar predictions! Contribute *Salmonella* genomes to SISTR!


You can contribute by:

- let us know here: https://github.com/phac-nml/sistr_cmd/issues/15
- linking to your genome on NCBI SRA/BioSample/Assembly
- contacting the authors of SISTR


Development
===========

Getting started

.. code-block:: bash
	
	git clone https://github.com/phac-nml/sistr_cmd.git
	cd sistr_cmd/
	export PYTHONPATH=$(pwd)
	# run tests
	py.test tests/

Pull requests for feature additions and bug fixes welcome!


Using ``sistr_cmd`` in your Python application
----------------------------------------------

Want to use ``sistr_cmd`` directly in your Python application?

Install ``sistr_cmd`` using pip or Conda.

You can run SISTR serovar predictions like so:

.. code-block:: python

	from sistr.sistr_cmd import sistr_predict
	# create mock commandline arguments class
	class SistrCmdMockArgs:
	    run_mash = True
	    no_cgmlst = False
	    qc = True
	    use_full_cgmlst_db = False
	# run SISTR serovar prediction
	sistr_results, allele_results = sistr_predict(genome_fasta_path, genome_name, keep_tmp=False, tmp_dir='/tmp/sistr_cmd', args=SistrCmdMockArgs)
	# use sistr_cmd results for something


License
=======

Copyright 2017 Public Health Agency of Canada

Distributed under the Apache 2.0 license.
