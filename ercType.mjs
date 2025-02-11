import { JsonRpcProvider } from 'ethers';
import { Contract } from 'sevm';
import 'sevm/4bytedb';
import { readFileSync } from 'fs';
import { parse } from 'csv-parse/sync';

// Create a provider instance.
const provider = new JsonRpcProvider('https://cloudflare-eth.com/');

// Read and parse the CSV file.
const csvData = readFileSync('contracts.csv', 'utf8');
const records = parse(csvData, {
  columns: true,
  skip_empty_lines: true
});

// Process only the first 100 rows.
const first100 = records.slice(0, 50);

for (const record of first100) {
  const address = record.address;
  console.log(`Processing contract at ${address}`);
  
  // Get the contract bytecode from the blockchain.
  const bytecode = await provider.getCode(address);
//   console.log(`Processing bytecode ${bytecode}`);

  // Check that the bytecode is not empty.
  if (!bytecode || bytecode === '0x' || bytecode === '0x0') {
    console.log(`Skipping ${address} because bytecode is empty.`);
    continue;
  }
  
  // Create and patch the contract instance.
  let contract;
  try {
    contract = new Contract(bytecode).patchdb();
  } catch (error) {
    console.error(`Error creating contract instance for ${address}:`, error);
    continue;
  }
  
  // Check for ERC compliance.
  console.log(`Address ${address}: isERC20: ${contract.isERC('ERC20')}`);
  console.log(`Address ${address}: isERC721:  ${contract.isERC('ERC721')}`);
  console.log(`Address ${address}: isERC1155:  ${contract.isERC('ERC1155')}`);


// if (
//     contract.isERC('ERC20') || 
//     contract.isERC('ERC721') || 
//     contract.isERC('ERC223') || 
//     contract.isERC('ERC777') || 
//     contract.isERC('ERC1155') || 
//     contract.isERC('ERC1046') || 
//     contract.isERC('ERC1363') || 
//     contract.isERC('ERC2309') || 
//     contract.isERC('ERC2612') || 
//     contract.isERC('ERC2981') || 
//     contract.isERC('ERC3525') || 
//     contract.isERC('ERC3643') || 
//     contract.isERC('ERC4400') || 
//     contract.isERC('ERC4519') || 
//     contract.isERC('ERC4626') || 
//     contract.isERC('ERC4906') || 
//     contract.isERC('ERC4907') || 
//     contract.isERC('ERC4910') || 
//     contract.isERC('ERC4955') || 
//     contract.isERC('ERC5006') || 
//     contract.isERC('ERC5007') || 
//     contract.isERC('ERC5023') || 
//     contract.isERC('ERC5169') || 
//     contract.isERC('ERC5192') || 
//     contract.isERC('ERC5267') || 
//     contract.isERC('ERC5375') || 
//     contract.isERC('ERC5380') || 
//     contract.isERC('ERC5484') || 
//     contract.isERC('ERC5489') || 
//     contract.isERC('ERC5507') || 
//     contract.isERC('ERC5521') || 
//     contract.isERC('ERC5528') || 
//     contract.isERC('ERC5570') || 
//     contract.isERC('ERC5585') || 
//     contract.isERC('ERC5606') || 
//     contract.isERC('ERC5615') || 
//     contract.isERC('ERC5679') || 
//     contract.isERC('ERC5725') || 
//     contract.isERC('ERC5773') || 
//     contract.isERC('ERC6059') || 
//     contract.isERC('ERC6066') || 
//     contract.isERC('ERC6105') || 
//     contract.isERC('ERC6147') || 
//     contract.isERC('ERC6150') || 
//     contract.isERC('ERC6220') || 
//     contract.isERC('ERC6239') || 
//     contract.isERC('ERC6381') || 
//     contract.isERC('ERC6454') || 
//     contract.isERC('ERC6672') || 
//     contract.isERC('ERC6808') || 
//     contract.isERC('ERC6809') || 
//     contract.isERC('ERC6982') || 
//     contract.isERC('ERC7160') || 
//     contract.isERC('ERC7231') || 
//     contract.isERC('ERC7401') || 
//     contract.isERC('ERC7409')
//   ) {
//     if (contract.isERC('ERC20')) {
//       console.log('Contract is compliant with: ERC20');
//     }
//     if (contract.isERC('ERC721')) {
//       console.log('Contract is compliant with: ERC721');
//     }
//     if (contract.isERC('ERC223')) {
//       console.log('Contract is compliant with: ERC223');
//     }
//     if (contract.isERC('ERC777')) {
//       console.log('Contract is compliant with: ERC777');
//     }
//     if (contract.isERC('ERC1155')) {
//       console.log('Contract is compliant with: ERC1155');
//     }
//     if (contract.isERC('ERC1046')) {
//       console.log('Contract is compliant with: ERC1046');
//     }
//     if (contract.isERC('ERC1363')) {
//       console.log('Contract is compliant with: ERC1363');
//     }
//     if (contract.isERC('ERC2309')) {
//       console.log('Contract is compliant with: ERC2309');
//     }
//     if (contract.isERC('ERC2612')) {
//       console.log('Contract is compliant with: ERC2612');
//     }
//     if (contract.isERC('ERC2981')) {
//       console.log('Contract is compliant with: ERC2981');
//     }
//     if (contract.isERC('ERC3525')) {
//       console.log('Contract is compliant with: ERC3525');
//     }
//     if (contract.isERC('ERC3643')) {
//       console.log('Contract is compliant with: ERC3643');
//     }
//     if (contract.isERC('ERC4400')) {
//       console.log('Contract is compliant with: ERC4400');
//     }
//     if (contract.isERC('ERC4519')) {
//       console.log('Contract is compliant with: ERC4519');
//     }
//     if (contract.isERC('ERC4626')) {
//       console.log('Contract is compliant with: ERC4626');
//     }
//     if (contract.isERC('ERC4906')) {
//       console.log('Contract is compliant with: ERC4906');
//     }
//     if (contract.isERC('ERC4907')) {
//       console.log('Contract is compliant with: ERC4907');
//     }
//     if (contract.isERC('ERC4910')) {
//       console.log('Contract is compliant with: ERC4910');
//     }
//     if (contract.isERC('ERC4955')) {
//       console.log('Contract is compliant with: ERC4955');
//     }
//     if (contract.isERC('ERC5006')) {
//       console.log('Contract is compliant with: ERC5006');
//     }
//     if (contract.isERC('ERC5007')) {
//       console.log('Contract is compliant with: ERC5007');
//     }
//     if (contract.isERC('ERC5023')) {
//       console.log('Contract is compliant with: ERC5023');
//     }
//     if (contract.isERC('ERC5169')) {
//       console.log('Contract is compliant with: ERC5169');
//     }
//     if (contract.isERC('ERC5192')) {
//       console.log('Contract is compliant with: ERC5192');
//     }
//     if (contract.isERC('ERC5267')) {
//       console.log('Contract is compliant with: ERC5267');
//     }
//     if (contract.isERC('ERC5375')) {
//       console.log('Contract is compliant with: ERC5375');
//     }
//     if (contract.isERC('ERC5380')) {
//       console.log('Contract is compliant with: ERC5380');
//     }
//     if (contract.isERC('ERC5484')) {
//       console.log('Contract is compliant with: ERC5484');
//     }
//     if (contract.isERC('ERC5489')) {
//       console.log('Contract is compliant with: ERC5489');
//     }
//     if (contract.isERC('ERC5507')) {
//       console.log('Contract is compliant with: ERC5507');
//     }
//     if (contract.isERC('ERC5521')) {
//       console.log('Contract is compliant with: ERC5521');
//     }
//     if (contract.isERC('ERC5528')) {
//       console.log('Contract is compliant with: ERC5528');
//     }
//     if (contract.isERC('ERC5570')) {
//       console.log('Contract is compliant with: ERC5570');
//     }
//     if (contract.isERC('ERC5585')) {
//       console.log('Contract is compliant with: ERC5585');
//     }
//     if (contract.isERC('ERC5606')) {
//       console.log('Contract is compliant with: ERC5606');
//     }
//     if (contract.isERC('ERC5615')) {
//       console.log('Contract is compliant with: ERC5615');
//     }
//     if (contract.isERC('ERC5679')) {
//       console.log('Contract is compliant with: ERC5679');
//     }
//     if (contract.isERC('ERC5725')) {
//       console.log('Contract is compliant with: ERC5725');
//     }
//     if (contract.isERC('ERC5773')) {
//       console.log('Contract is compliant with: ERC5773');
//     }
//     if (contract.isERC('ERC6059')) {
//       console.log('Contract is compliant with: ERC6059');
//     }
//     if (contract.isERC('ERC6066')) {
//       console.log('Contract is compliant with: ERC6066');
//     }
//     if (contract.isERC('ERC6105')) {
//       console.log('Contract is compliant with: ERC6105');
//     }
//     if (contract.isERC('ERC6147')) {
//       console.log('Contract is compliant with: ERC6147');
//     }
//     if (contract.isERC('ERC6150')) {
//       console.log('Contract is compliant with: ERC6150');
//     }
//     if (contract.isERC('ERC6220')) {
//       console.log('Contract is compliant with: ERC6220');
//     }
//     if (contract.isERC('ERC6239')) {
//       console.log('Contract is compliant with: ERC6239');
//     }
//     if (contract.isERC('ERC6381')) {
//       console.log('Contract is compliant with: ERC6381');
//     }
//     if (contract.isERC('ERC6454')) {
//       console.log('Contract is compliant with: ERC6454');
//     }
//     if (contract.isERC('ERC6672')) {
//       console.log('Contract is compliant with: ERC6672');
//     }
//     if (contract.isERC('ERC6808')) {
//       console.log('Contract is compliant with: ERC6808');
//     }
//     if (contract.isERC('ERC6809')) {
//       console.log('Contract is compliant with: ERC6809');
//     }
//     if (contract.isERC('ERC6982')) {
//       console.log('Contract is compliant with: ERC6982');
//     }
//     if (contract.isERC('ERC7160')) {
//       console.log('Contract is compliant with: ERC7160');
//     }
//     if (contract.isERC('ERC7231')) {
//       console.log('Contract is compliant with: ERC7231');
//     }
//     if (contract.isERC('ERC7401')) {
//       console.log('Contract is compliant with: ERC7401');
//     }
//     if (contract.isERC('ERC7409')) {
//       console.log('Contract is compliant with: ERC7409');
//     }
//   } else {
//     console.log('Contract does not match any of the specified ERC standards.');
//   }
  
}

