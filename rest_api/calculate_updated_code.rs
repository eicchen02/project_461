/*  Name: Matthew Nale
 *  Date of Last Edit: 3/25/2023
 *  
 *  Purpose: Calculate the amount of code introduced through pull requests compared to the overall size of the project
 *
 *  Details: Using data from the pull requests of the repo, find the fraction of new code being introduced through commits from pull requests
*/
use std::env;
use std::fs::File; //rust file library
use std::process::Command; //library to run processes in rust
use std::io::BufWriter;
use std::io::Write;

fn main(){
    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //create a variable for the file path and save the first command line argument into it
    let url = &cli_input[1]; 

    //open new logfiles after cleaning old ones
    let mut log2 = BufWriter::new(File::open("log/logv2.txt").expect("Error creating log2 file!"));

    //open output file to write bus factor scores to
    let mut out_file = BufWriter::new(File::create("output/updatedcode_out.txt").expect("Error opening output for updated code!"));

    //Call information with rest_api functions for each url

    let fractionnew = Command::new("python3").arg("rest_api/pullRequests.py").arg(url).output().expect("Err");
    write!(log2, "\nFraction of code released through pull requests for url {}: {:?}\n", url, &fractionnew.stdout).expect("Error writing to log");
        
	let mut fraction_new = String::from_utf8(fractionnew.stdout).unwrap();
    fraction_new.pop();
	let updated_code : f64 = fraction_new.parse().unwrap();

    write!(log2, "UpdatedCode score for url {}: {:.2}\n\n", url, updated_code).expect("Error writing to log");
    write!(out_file, "{0}\n", updated_code).expect("Error writing updated code score to output");
}
