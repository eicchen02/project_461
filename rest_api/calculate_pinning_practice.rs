/*  Name: Jack Kwan
 *  Date of Last Edit: 4/15/2023
 *  
 *  Purpose: Calculate the Pinning Practice Submetric for a Github Repo
 *
 *  Details: Using provided data, calculates the Pinning Practice Score in the range of [0,1], with 1 representing the repo having zero dependencies pinned to a major + minor version  
*/
use std::env;
use std::fs; //rust file library
use std::fs::File; //rust file library
use std::process::Command; //library to run processes in rust
use std::io::BufWriter;
use std::path::Path;
use std::io::Write;

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

    let mut output_text = BufWriter::new(File::create("output/pinningpractice_out.txt").expect("Error opening output for pinning practice metric."));

    let pinningpractice_inst = Command::new("python3").arg("rest_api/versionpinning.py").arg(url).output().expect("Err");
    write!(log2, "\nFraction of dependencies pinned to a major and minor version for url {}: {:?}\n", url, pinningpractice_inst.stdout).expect("Error writing to log");
    
    let mut pinningpractice_str = String::from_utf8(pinningpractice_inst.stdout).unwrap();
    pinningpractice_str.pop();
    let version_pinning_full : f64 = pinningpractice_str.parse().unwrap();

    write!(log2, "Good Pinning Practice score for url {}: {:.2}\n\n", url, version_pinning_full).expect("Error writing to log");
    write!(output_text, "{0}\n", version_pinning_full).expect("Error writing version pinning score to output");

}
