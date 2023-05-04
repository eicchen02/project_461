/*  Name: Jack Kwan
 *  Date of Last Edit: 2/12/2023
 *  
 *  Purpose: Calculate Bus Factor Sub Metric of a given Github Repository
 *
 *  Details: Using provided data, calculates the Busfactor in the range of [0,1], with 1 being each contributor being most valuable upon replacement 
*/
use std::env;
use std::fs; //rust file library
use std::fs::File; //rust file library
use std::process::Command; //library to run processes in rust
use std::io::BufWriter;
use std::path::Path;
use std::io::Write;

//calculate_busfactor will determine the Bus Factor weighting for the Net Score total
pub fn calculate_busfactor(numcommits: f64, numcontributors: f64, numfiles: f64) -> f64{

    let busfactor: f64;
    busfactor = (0.5) * ((numcontributors / numcommits) + (numcontributors / numfiles)); //Calculate the score as an average between two metrics
    if busfactor > 1.0 {
        return 1.0;
    }
    else {
        return f64::trunc(busfactor * 10.0) / 10.0;
    }   
}

fn main(){
    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //create a variable for the file path and save the first command line argument into it
    let url = &cli_input[1]; 

    //if the logfiles exist from a previous run, delete them
    let is_logv1 = Path::new("log/logv1.txt").exists();
    if is_logv1 == true{
        
        //remove old log1 file and handle error
        let _remove_log1 = match fs::remove_file("log/logv1.txt"){
            Ok(_remove_log1) => _remove_log1,
            Err(..) => {
                println!("Error deleting old log1 file!\n");
                std::process::exit(1);
            }
        };
    }
    let is_logv2 = Path::new("log/logv2.txt").exists();
    if is_logv2 == true{

        //remove old log2 file and handle error
        let _remove_log2 = match fs::remove_file("log/logv2.txt"){
            Ok(_remove_log2) => _remove_log2,
            Err(..) => {
                println!("Error deleting old log2 file!\n");
                std::process::exit(1);
            }
        };
    }

    //open new logfiles after cleaning old ones
    let mut log2 = BufWriter::new(File::create("log/logv2.txt").expect("Error creating log2 file!"));

    //open output file to write bus factor scores to
    let mut out_file = BufWriter::new(File::create("output/busfactor_out.txt").expect("Error opening output file for busfactor"));


    //Call information with rest_api functions for each url
    let numcommits = Command::new("python3").arg("rest_api/totalCommits.py").arg(url).output().expect("Err");
    write!(log2, "\nNumber of commits for url {}: {:?}\n", url, numcommits.stdout).expect("Error writing to log");
    let numcontributors = Command::new("python3").arg("rest_api/totalContributors.py").arg(url).output().expect("Err");
    write!(log2, "\nNumber of contributors for url {}: {:?}\n", url, numcontributors.stdout).expect("Error writing to log");
    let numfiles = Command::new("python3").arg("rest_api/totalFiles.py").arg(url).output().expect("Err");
    write!(log2, "\nNumber of files for url {}: {:?}\n", url, numfiles.stdout).expect("Error writing to log");

	let mut num_commits = String::from_utf8(numcommits.stdout).unwrap();
	num_commits.pop();

	let mut num_contributors = String::from_utf8(numcontributors.stdout).unwrap();
	num_contributors.pop();

	let mut num_files = String::from_utf8(numfiles.stdout).unwrap();
	num_files.pop();

    let contributor_score = calculate_busfactor(num_commits.parse().unwrap(), num_contributors.parse().unwrap(), num_files.parse().unwrap());
    write!(log2, "BusFactor score for url {}: {:.2}\n\n", url, contributor_score).expect("Error writing to log");
    write!(out_file, "{0}\n", contributor_score).expect("Error writing busfactor to output");
}
