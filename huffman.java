import java.io.File;
import java.util.Scanner;
import java.lang.StringBuffer;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.util.Map;
import java.util.HashMap;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.PriorityQueue;
import java.util.Comparator;

public class huffman {
	
	public static class Node implements Comparable<Node> {
       	/* Node represents each character in Huffman tree. */
        	/* Weight is symbol frequency */
		int weight;
		String symbol;
		Node left, right;
		
		public Node (int weight, String symbol) {
			this (weight, symbol, null, null);
		}

		public Node (int weight, String symbol, Node l, Node r) {
			this.weight = weight;
			this.symbol = symbol;
			left = l;
			right = r;
		}

		public int compareTo (Node n) {
			return this.weight - n.weight;
		}
	}

	public static void createLookup (Map<String, String> lookup, Node n, String s) {
 		/* Generate corresponding bits for each character. */
		if (n.left == null && n.right == null) 
			lookup.put (n.symbol, s);
		else {
			createLookup (lookup, n.left, s + '0');
			createLookup (lookup, n.right, s + '1');
		}

	}
			
	public static void main (String[] args) {
		/* args;
		  args[0] - File to compress.
		  args[1] - Compressed filename.
		  args[2] - Decompressed file.
		*/
		File source = new File (args[0]);
		StringBuffer text = new StringBuffer();
		try {
			/* Copy text file to buffer */	
			Scanner scanner = new Scanner (source);
			while (scanner.hasNext())
				text.append (scanner.nextLine());
			System.out.println("File opened...");


			/* Count character frequencies */
			Map<String, Integer> map = new HashMap<String, Integer>();
			for (int i = 0; i < text.length(); i++) {
				String c = new Character(text.charAt (i)).toString();
				if (!map.containsKey (c))
					map.put (c, 0);
				map.put (c, map.get(c) + 1);
			}

			/* Print results */
			System.out.println("Character Frequencies - ");
			SortedSet<String> keys = new TreeSet<String>(map.keySet());
			for (String key : keys) {
				int freq = map.get(key);
				if (key.equals (" "))
					key = "Space";
				System.out.format ("%-6s%3d%n", key, freq);
			}
			System.out.println("\nTotal characters: " + text.length() + "  (" + 8 * text.length() + " bits)\n");

			/* Build Huffman trie */
			PriorityQueue<Node> pq = new PriorityQueue<Node> ();
			Node EOF = new Node (0, "^");
			pq.add (EOF);

			/* Build a forest of trees */
			for (String key : keys) {
				int weight = map.get(key);
				Node n = new Node (weight, key);
				pq.add (n);
			}
			/* Merge two smallest trees */
			while (pq.size() != 1) {
				Node t1 = pq.poll();
				Node t2 = pq.poll();
				Node T = new Node(t1.weight + t2.weight, "parent", t1, t2);
				pq.add (T);
			}
			/* Create lookup table */
			Node root = pq.poll();
			Map<String, String> lookup = new HashMap<String, String>();
			createLookup (lookup, root, "");	
			
			/* Print table */
			System.out.println("Lookup Table - ");
			keys = new TreeSet<String>(lookup.keySet());
			for (String key : keys) {
				String code = lookup.get(key);
				System.out.println(key + " '" + code + "'");
			}

			/* Compress file */
			String newText = "";
			for (int i = 0; i < text.length(); i++) {
				String c = new Character(text.charAt(i)).toString();
				newText += lookup.get(c);
			}

			/* Add EOF */
			newText += lookup.get ("^");
			int length= newText.length();
			for (int i = 0; i < (length % 8); i++)
				newText += "0";

			/* Print comparison */
			System.out.println("\nOriginal Text - ");
			System.out.println(text);
			System.out.println("\nCompressed Text - ");
			System.out.println(newText + " (" + newText.length() + " bits)");

			/* Build file */
			// System.out.println("\nHere are the bytes:");
			byte[] bytes = new byte[newText.length() / 8];
			for (int i = 0; i < newText.length() / 8; i++) {
				String compressedByte = newText.substring (i * 8, (i + 1) * 8);
				byte b = (byte) Integer.parseInt (compressedByte, 2);
				// System.out.println(compressedByte + ' ' + b);
				bytes[i] = b;
			}

			/* Write compressed bytes */
			File file = new File(args[1]);
			FileOutputStream fop = new FileOutputStream(file);
			fop.write (bytes);
			fop.flush();
			fop.close();

			/* Read bytes to decompress */
			System.out.println("\nReading bytes...");
			File newFile = new File (args[2]);
			FileInputStream fin = new FileInputStream (file);
			String encoded = "";
			int content;
			while ((content = fin.read()) != -1) {
				String b = Integer.toBinaryString (content);
				b = String.format ("%8s", b).replace (" ", "0");
				//System.out.println(b + ' ' + (byte)content);	
				encoded += b;
			}
			System.out.println("\nRead Text - ");
			System.out.println(encoded);

			/* Decode file */
			String decoded = "";
			int index = 0;
			while (!decoded.endsWith("^")) {
				Node node = root;
				while (node.left != null && node.right != null) {
					if (encoded.charAt (index) == '1')
						node = node.right;
					else
						node = node.left;
					index += 1;
				}
				decoded += node.symbol;
			}
			decoded = decoded.substring (0, decoded.length() - 1) + "\n";
			System.out.println("\nDecoded Text - ");
			System.out.println(decoded);

			/* Write decoded file */
			File decodedFile = new File (args[2]);
			fop = new FileOutputStream (decodedFile);
			fop.write (decoded.getBytes());
			fop.flush();
			fop.close();

		} catch (Exception e) {
			System.out.println (args[0] + ": File not found.");
		}

	}
}
