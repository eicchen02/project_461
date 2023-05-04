use std::env; //rust stdlib function to get command line args
use std::fs; //rust file library
use std::fs::File; //rust file library
use std::process::Command; //library to run processes in rust
use std::io::BufWriter;
use tokei::{Config, Languages, LanguageType};
use std::path::Path;
use std::io::Write;
use std::panic;

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
    
    //check if the cloned repos folder is already there from a previous run, and delete it if so
    let is_cloned_repos = Path::new("local_cloning/cloned_repos/").exists();
    if is_cloned_repos == true{
        
        //cleans out old repos if theyre still there
        let _remove_old_clones = match fs::remove_dir_all("local_cloning/cloned_repos/"){
            Ok(_remove_old_clones) => _remove_old_clones,
            Err(..) => {
                println!("Error deleting old cloned repos!\n");
                std::process::exit(1);
            }
        };
    }
    
    //run clone_repo.py
    let _run_clone_script = Command::new("python3").arg("local_cloning/clone_repo.py").arg(&url).status().expect("Err");

    //if the clone script didnt return success, exit 1 and print error
    if _run_clone_script.success() == false {
        println!("Error cloning repos!");
        std::process::exit(1);
    }

    //open up the directory with all the cloned repos
    let cloned_folders = match fs::read_dir("local_cloning/cloned_repos/"){
        Ok(cloned_folders) => cloned_folders,
        Err(..) => {
            println!("Error opening up cloned repos directory!\n");
            std::process::exit(1);
        }
    };

    //initialize a counter for the current folder number
    let mut folder_num = 1;

    //open output file to write rampup scores to
    let mut out_file = BufWriter::new(File::create("output/rampup_out.txt").expect("Error opening output file for rampup"));

    //loop through all folders in "cloned_repos"
    for folder in cloned_folders {
        //get the path of the current folder
        let _folder_path = (folder.unwrap().path().display()).to_string(); 

        //initialize parameters for when we use tokei to parse the folders and count code/comments
        let paths = &[_folder_path]; //folder to search
        let excluded = &[]; //folders excluded from the search
        let config = Config::default(); //configure the parser to default

        //configure the tokei language to be javascript 
        let mut languages = Languages::new();
        languages.get_statistics(paths, excluded, &config);
        panic::set_hook(Box::new(|_info| {}));
        let js = panic::catch_unwind(|| &languages[&LanguageType::JavaScript]);

        if js.is_ok(){
            //get the number of lines of code and comments and log them
            let result = js.unwrap();
            let code_lines = result.code;
            let comment_lines = result.comments;
            write!(log2, "\nLines of code in folder {}: {}\n", folder_num, code_lines).expect("Error writing to log");
            write!(log2, "Lines of comments in folder {}: {}\n", folder_num, comment_lines).expect("Error writing to log");
        

            //calculate rampup and log it
            let code_u32 = u32::try_from(code_lines).unwrap();
            let comment_u32 = u32::try_from(comment_lines).unwrap();
            let ramp_up = calculate_ramp_up(code_u32, comment_u32);
            write!(log2, "RampUp score for repo {}: {:.2}\n\n", folder_num, ramp_up).expect("Error writing to log");
        
            //write the rampup score to the rampup_out.txt file in the output folder
            write!(out_file, "{0}\n", ramp_up).expect("Error writing rampup to output");
        }
        else{
            write!(log2, "\nNo Javascript in folder {}\n", folder_num).expect("Error writing to log");
            
            write!(out_file, "0.0\n").expect("Error writing rampup to output");
        }
        //increment the folder counter
        folder_num+=1;
    }
}

//this function takes the number of code lines, and comment lines and calculates the rampup score
fn calculate_ramp_up(lines_of_code: u32, lines_of_comments: u32) -> f32{

    //calculate RampUp score using our formula
    let float_code= lines_of_code as f32;
    let float_comments = lines_of_comments as f32;
    let calculated_score: f32 = 2.0 * (float_comments / float_code);

    //return 1 if the calculated score was greater than 1 and return the calculated score if it was less than 1
    if calculated_score > 1.0 {
        return 1.0;
    } else {
        return calculated_score;
    }

}

