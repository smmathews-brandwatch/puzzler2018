#!/usr/bin/perl
#
# Hexey bot implemented in perl5 with Dijkstra algorithm.
# Author: Damian Nardelli
#
# Explanation
#   In 'JSON Endpoints' section below you will find the routines to interact with the Puzzler Server.
#   In 'Graph Management' section below you will find the actual implementation to guess the best next move to make.
#   
#   Given the following 4x4 board:
#
#       0 1 2 3
#       _ _ _ _
#    0 |e     c|
#    1 |  h    |
#    2 |b   c  |
#    3 |_ _ _ _|
#
#     (h) Hexey bot can be found at 1x1
#     (b) Bot base can be found at 0x2
#     (e) Enemy can be found at 0x0
#     (c) Collectibles can be found at 0x3 and 2x2 
#   
#    Please notice the graph below that would be created to represent the possible movements for the above board:
#
#       0   1   2   3
#    0  e   o - o - c
#           |   |   |
#    1  o - h - o - o
#           |   |   |
#    2  b   o - c - o
#           |   |   |
#    3  o - o - o - o
#
#     The graph is directed. A vertex represents an entity. An edge represents a possible transition from one vertex to another.
#     My initial idea was to implement a simple BFS search (https://en.wikipedia.org/wiki/Breadth-first_search) from Hexey's vertex to 
#     all collectibles, and then focus on the collectible with the shortest path.
#     I ended up running a Dijkstra search on an unweighted graph as the Graph framework that I'm using doesn't have a simple BFS search implementation.
#     You may find more details about this in https://metacpan.org/pod/distribution/Graph/lib/Graph.pod#Single-Source-Shortest-Paths-(SSSP)
#     and https://en.wikipedia.org/wiki/Dijkstra's_algorithm
#     Moreover, if we added a weight to each vertex as explained in _Future Improvements_ section, then we would need to use Dijkstra algorithm.
#
#     Next, the bot will head to that collectible by following the shortest path discovered through Dijkstra algorithm. And this will be
#     re-calculated every time a tick is sent, because the other enemies movements may affect / block our shortest path.
#     This will be executed as long as our backpack is not full. If the backpack is full, then the only possible vertex to go will be the base bot.
#
# Required Modules
#   - Graph (https://metacpan.org/pod/distribution/Graph/lib/Graph.pod#NAME)
#   - LWP::UserAgent (https://metacpan.org/pod/LWP::UserAgent#NAME)
#   - JSON::decode_json (https://metacpan.org/pod/JSON#decode_json)
#   You may want to install the missing modules through cpan as follows:
#   sudo cpan install Graph; sudo cpan install JSON;
# 
# Future Improvements
#   We could calculate the _Opportunity of Investment_ for all collectibles, based on the following characteristics:
#   Pros:
#   a) Distance from bot to item X
#   b) Distance from item X to all other items {0,..,X-1,X+1,...,N-1}
#   Cons:
#   c) Distance from item X to base. The more items have been picked up, the more important this cons will be.
#   d) Distance from item X to other enemies. Why will we try to pick up an element close to enemies? Maybe it's a waste of time and resources (frames).
#   Variables:
#   e) Backpack size
#   We should define an _Opportunity of Investment_ formula to give an score to each item. Then our graph will be weighted from now on. 
# 
# Begin of hexeyBot.pl

use JSON qw( decode_json );
use LWP::UserAgent;
use Graph;

my $ua = LWP::UserAgent->new;

print "Starting...\n";

for (;;) {
  my $state = getState();
  my $nextMove = getNextMove($state);
  if ($nextMove eq 'none') {
    print "round# " . $state->{'simRound'} . ": rescued=" . $state->{'score'}->{'rescued'} . " lost=" . $state->{'score'}->{'lost'} . "\n";
    newSimulator();
  } else {
    sendTick($nextMove);
  }
}

################################################################
# Graph Management
################################################################

sub getMeta {
  my ($graph, $state) = @_;
  for $x (0..$state->{'board'}->{'width'} - 1) {
    for $y (0..$state->{'board'}->{'height'} - 1) {
      my $vId = getVertexId($x, $y);
      $graph->set_vertex_attributes($vId, { boardPiece => 'empty' });
    }
  }
  my %meta;
  for my $e (@{$state->{'board'}->{'entities'}}) {
    if (!defined($e->{'ownerId'})) {
      my $vId = getVertexId($e->{'position'}->{'x'}, $e->{'position'}->{'y'});
      $meta{'bot'} = $vId if ($e->{'boardPiece'} eq 'bot');
      push @{$meta{'candidates'}}, $vId if ($e->{'boardPiece'} eq 'collectible');
      $meta{'botBase'} = $vId if ($e->{'boardPiece'} eq 'bot_base');
    } else {
      $meta{'backpack'} = $meta{'backpack'} + 1 if ($e->{'boardPiece'} eq 'collectible' && $e->{'ownerId'} eq 0);
    }
  }

  $meta{'backpackFull'} = $meta{'backpack'} >= $state->{'maxCollectibles'};
  @{$meta{'candidates'}} = ($meta{'botBase'}) if ($meta{'backpackFull'} || (!defined($meta{'candidates'}) && $meta{'backpack'} > 0));
  return %meta;
}

sub addVertices {
  my ($graph, $state) = @_;
  for my $e (@{$state->{'board'}->{'entities'}}) {
    # Ignoring the items that were already picked up
    if (!defined($e->{'ownerId'})) {
      my $vId = getVertexId($e->{'position'}->{'x'}, $e->{'position'}->{'y'});
      $graph->set_vertex_attributes($vId, $e);
    }
  }
}

sub addEdges {
  my ($graph, $state, %meta) = @_;
  for $x (0..$state->{'board'}->{'width'} - 1) {
    for $y (0..$state->{'board'}->{'height'} - 1) {
      my $vId = getVertexId($x, $y);
      my $e = $graph->get_vertex_attributes($vId);
      my $isEntityBotOrEmpty = $e->{'boardPiece'} eq 'bot' || $e->{'boardPiece'} eq 'empty';
      my $isEntityValidCollectible = $e->{'boardPiece'} eq 'collectible' && !$meta{'backpackFull'};
      if ($isEntityBotOrEmpty || $isEntityValidCollectible) {
        my ($vId_l, $vId_r, $vId_u, $vId_d) = (getVertexId($x - 1, $y), getVertexId($x + 1, $y), getVertexId($x, $y - 1), getVertexId($x, $y + 1));
        $graph->add_edge($vId, $vId_l) if ($graph->has_vertex($vId_l));
        $graph->add_edge($vId, $vId_r) if ($graph->has_vertex($vId_r));
        $graph->add_edge($vId, $vId_u) if ($graph->has_vertex($vId_u));
        $graph->add_edge($vId, $vId_d) if ($graph->has_vertex($vId_d));
      }
    }
  }
}

sub getNextMove { 
  my ($state) = @_;
  my $graph = Graph->new;
  my %meta = getMeta($graph, $state);
  # If no candidates are found, then we have no move to make
  if (!defined($meta{'candidates'})) {
    return 'none';
  }

  addVertices($graph, $state);
  addEdges($graph, $state, %meta);

  print "Graph: $graph\n";

  my @candidatePaths;
  for my $c (@{$meta{'candidates'}}) {
    push @candidatePaths, [$graph->SP_Dijkstra($meta{'bot'}, $c)];
  }
  my @candidatePathsSorted = sort {@$a <=> @$b} @candidatePaths;
  my $candidateVertex = ${$candidatePathsSorted[0]}[1];

  print "Candidate Vertex is " . $candidateVertex . "\n";

  return 'none' if (!defined $candidateVertex || $candidateVertex eq '');

  my ($vertexBotX, $vertexBotY) = getPositions($meta{'bot'});
  my ($vertexCollectibleX, $vertexCollectibleY) = getPositions($candidateVertex);
  return 'left' if ($vertexBotX > $vertexCollectibleX);
  return 'right' if ($vertexBotX < $vertexCollectibleX);
  return 'up' if ($vertexBotY > $vertexCollectibleY);
  return 'down' if ($vertexBotY < $vertexCollectibleY);
  return 'none';
}

sub getVertexId {
  my ($x, $y) = @_;
  return $x . 'x' . $y;
}

sub getPositions {
  my ($vertexId) = @_;
  return split 'x', $vertexId;
}

################################################################
# JSON Endpoints
################################################################

sub getState {
  my $response = $ua->get('http://localhost:5000/simulator/state');
  return processResponse($response);  
}

sub newSimulator {
  my $response = $ua->post('http://localhost:5000/simulator/new');
  return processResponse($response);
}

sub getRoundScores {
  my $response = $ua->get('http://localhost:5000/roundScores');
  return processResponse($response);
}

sub sendTick {
  my ($action) = @_;
  my $response = $ua->post('http://localhost:5000/simulator/tick', 'Content-Type' => 'application/json', Content => '{"entityIdsToAction":[{"id":0,"action":"' . $action . '"}]}');
  return processResponse($response);
}

sub processResponse {
  my ($response) = @_;
  if (!$response->is_success) {
    die "$url failed";
  }
  my $requestStr = $response->request->as_string;
  my $responseStr = $response->as_string;
  print "\n";
  print "$requestStr\n";
  print "$responseStr\n";
  print "--------------------------------------------\n";
  if ($response->as_string =~ /all rounds done/) { 
    print "Looks like I'm all done here.\n";
    die;
  }
  return decode_json($response->decoded_content);
}


# End of hexeyBot.pl

