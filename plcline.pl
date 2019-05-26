#!/usr/bin/perl -w
#use strict ;
my @linein=<> ;
my @colors=("\033[1;31m", "\033[1;32m", "\033[1;34m", "\033[38;5;208m", "\033[38;5;137m", "\033[38;5;109m", "\033[38;5;119m", "\033[38;5;129m", "\033[38;5;139m", "\033[38;5;149m", "\033[38;5;159m", "\033[38;5;169m", "\033[38;5;179m", "\033[38;5;189m", "\033[38;5;199m", "\033[38;5;220m", "\033[38;5;221m", "\033[38;5;222m", "\033[38;5;223m", "\033[38;5;224m", "\033[38;5;225m") ;
foreach(@linein){
	my $cp = 0 ;
	my @aline = split(// , $_) ;
	my $i=-1 ;
	my $thisis = "NULL" ;
	my $colorn = @colors ;
	foreach(@aline){
		if($_ eq "" ){ next ; }
		if(/-/ && $thisis eq "space" ){
		}elsif(/-/ && $thisis eq "NULL" ){
		}elsif(/-/ && $thisis eq "char" ){
						$thisis = "space" ;
						$cp++ ;
		}elsif(/_/ && $thisis eq "space" ){
		}elsif(/_/ && $thisis eq "NULL" ){
		}elsif(/_/ && $thisis eq "char" ){
						$thisis = "space" ;
						$cp++ ;
		}elsif(/\./ && $thisis eq "space" ){
		}elsif(/\./ && $thisis eq "NULL" ){
		}elsif(/\./ && $thisis eq "char" ){
						$thisis = "space" ;
						$cp++ ;
		}elsif(/\:/ && $thisis eq "space" ){
		}elsif(/\:/ && $thisis eq "NULL" ){
		}elsif(/\:/ && $thisis eq "char" ){
						$thisis = "space" ;
						$cp++ ;
		}elsif(/\// && $thisis eq "space" ){
		}elsif(/\// && $thisis eq "NULL" ){
		}elsif(/\// && $thisis eq "char" ){
						$thisis = "space" ;
						$cp++ ;
		}elsif(/\S/ && $thisis eq "space" ){ 
			$cp++ ; 	$thisis = "char" ;
		}elsif(/\S/ && $thisis eq "NULL" ){ 
						$thisis = "char" ;
		}elsif(/\S/ && $thisis eq "char" ){ 
		}elsif(/\s/ && $thisis eq "space" ){
		}elsif(/\s/ && $thisis eq "NULL" ){
		}elsif(/\s/ && $thisis eq "char" ){
						$thisis = "space" ;
		}
		if( $cp > 20 ){ $cp=0 ; }
		if(!(defined($colors[$cp]))){
			print "--->>> colors cp , cp=$cp<<<---\n" ;
		} elsif(!(defined($_))){
			print "\$_ is not good\n" ;
		}
		print "$colors[$cp]".$_."\033[0m";
	}
	#print "|\n" ;
}
# "\033[0m "
#{
#	print b119($1), green($2), blue($3), brown($4), b137($5), b109($6), b119($7), b129($8), b139($9), b220($10), b221($11), b222($12), b223($13), b224($14),b225($15)
#}

